import os

import pandas as pd
import numpy as np
from tqdm import tqdm

from pipelines.p2_aggregate_orca import WRITE_DIR as p2_write_dir
from pipelines.p4_aggregate_apc import WRITE_DIR as p4_write_dir
from pipelines.p4_aggregate_apc import OUTPUT_FILENAME as p4_fname
from utils import constants, data_utils
import statistics, csv

NAME = 'p5_orca_rates'

OUTPUT_FILENAME = f'{NAME}.csv'
WRITE_DIR = constants.PIPELINE_OUTPUTS_DIR

TOLERANCE_INTERVAL = [0.1, 1]


def load_input():
    """
    Load the specified datasets.
    """

    # Load data
    path1 = os.path.join(p2_write_dir, 'stops_aggregate.csv')
    path2 = os.path.join(p2_write_dir, 'routes_aggregate.csv')
    path3 = os.path.join(p4_write_dir, p4_fname)
    stops_df = pd.read_csv(path1)
    routes_df = pd.read_csv(path2)
    apc_df = pd.read_csv(path3)

    # Parse
    routes_df['stop_ids'] = routes_df['stop_ids']\
        .apply(lambda x: data_utils.parse_collection(x, set, int))
    stops_df['route_ids'] = stops_df['route_ids']\
        .apply(lambda x: data_utils.parse_collection(x, set, int))

    # Filter
    routes_df = routes_df[routes_df['route_id'].isin(set(apc_df['route_id']))]
    stops_df = stops_df[[
        all([y in set(apc_df['route_id']) for y in x])
        for x in stops_df['route_ids']
    ]]

    routes_df = routes_df.reset_index(drop=True)
    stops_df = stops_df.reset_index(drop=True)
    return stops_df, routes_df, apc_df


def attach_r_initial(stops_df, apc_df):
    """
    Adds the initial ORCA rate (r_initial) to the stops dataset, taking a
    weighted average by apc count when multiple routes go through a stop.
    """

    routes = {
        x[0]: {'n_apc': x[1], 'r_initial': x[3]}
        for x in apc_df.to_numpy()
    }

    stops = {
        x[0]: {
            'orca_count': x[1],
            'route_ids': x[2],
            'tract_num': x[3],
            'tract_population': x[4]
        }
        for x in stops_df.to_numpy()
    }
    stops = {x: stops[x] for x in stops if len(stops[x]['route_ids']) > 0}

    for stop_id in stops:
        route_ids = stops[stop_id]['route_ids']

        if len(route_ids) == 1:
            route_id = list(route_ids)[0]
            stops[stop_id]['r_initial'] = routes[route_id]['r_initial']

        else:
            r = [routes[route_id]['r_initial'] for route_id in route_ids]
            w = [routes[route_id]['n_apc'] for route_id in route_ids]

            stops[stop_id]['r_initial'] = np.average(r, weights=w)

    cols = list(stops_df.columns) + ['r_initial']
    result = [
        [stop_id] + [stops[stop_id][cols[i]] for i in range(1, len(cols))]
        for stop_id in stops
    ]
    return pd.DataFrame(result, columns=cols)


def attach_r_final(stops_df, routes_df, apc_df):
    """
    Calculates r_final.
    """

    # stop_id: (observed orca count, tract population)
    stops_map = {x[0]: (x[1], x[4]) for x in stops_df.to_numpy()}

    # route_id: (n_apc, n_orca, orca_rate)
    apc_map = {x[0]: (x[1], x[2], x[3]) for x in apc_df.to_numpy()}

    r_final_map = dict()
    error = np.array([])

    for row in routes_df.to_numpy():
        route, stops = (row[0], list(row[1]))

        stops = [x for x in stops if x in stops_map]
        if not stops:
            continue  # This only happens for 1 of the 155 routes

        r = apc_map[route][2]  # target overall rate
        o = np.array([stops_map[x][0] for x in stops])  # observed orca counts
        p = np.array([stops_map[x][1] for x in stops])  # tract populations

        # The ORCA rate expected values at each stop
        r_hat = r * (np.sum(p) * o) / (np.sum(o) * p)

        error = np.append(error, np.array([np.abs(x - r) for x in r_hat]))

        for i, stop in enumerate(stops):
            r_final_map[stop] = np.average([r_final_map[stop], r_hat[i]]) \
                if stop in r_final_map else r_hat[i]

    result = []
    ignored, total = (0, 0)
    for row in stops_df.to_numpy():
        stop_id = row[0]
        tract_num = row[3]
        tract_pop = row[4]
        r_initial = row[5]
        r_final = r_final_map[stop_id]

        if not TOLERANCE_INTERVAL[0] < r_final < TOLERANCE_INTERVAL[1]:
            r_final = r_initial  # backoff to r_inital if not within tolerance
            ignored += 1

        result.append([stop_id, tract_num, tract_pop, r_initial, r_final])
        total += 1

    tqdm.write(f'MAE: {np.average(error)}')
    tqdm.write(f'RMSE: {np.sqrt(np.average(error ** 2))}')
    tqdm.write(f'Rate within tolerance: {(total - ignored) / total}')

    cols = ['stop_id', 'tract_num', 'tract_population', 'r_initial', 'r_final']
    return pd.DataFrame(result, columns=cols)


def aggregate_by_tracts(stops_df):
    """
    Aggregates r_final by tract.
    """
    tr_rates = {}

    for stop in stops_df.to_numpy():
        tract = str(int(stop[1]))
        if tract not in tr_rates:
            tr_rates[tract] = []
        tr_rates[tract].append(stop[4])
    aggregate = []
    for tr in tr_rates:
        l = [tr, statistics.mean(tr_rates[tr])]
        aggregate.append(l)
    aggregate = np.array(aggregate)
    CENSUS_OUTPUT_DATA_DIR = os.path.join(constants.DATA_DIR, 'census_data', 'pipeline_output')
    with open(f'{CENSUS_OUTPUT_DATA_DIR}/tract_rates.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(aggregate)
    return aggregate

def run_pipeline():
    """
    Aggregates the APC and predicted ORCA rates by known routes.
    """

    # Run pipeline
    stops_df, routes_df, apc_df = load_input()
    stops_df = attach_r_initial(stops_df, apc_df)
    stops_df = attach_r_final(stops_df, routes_df, apc_df)
    stops_df = aggregate_by_tracts(stops_df)

    return stops_df


if __name__ == '__main__':
    run_pipeline()
