import os

import pandas as pd
import numpy as np
from tqdm import tqdm

from pipelines.p2_aggregate_orca import WRITE_DIR as p2_write_dir
from pipelines.p4_aggregate_apc import WRITE_DIR as p4_write_dir
from pipelines.p4_aggregate_apc import OUTPUT_FILENAME as p4_fname
from utils import constants, data_utils

NAME = 'p5_orca_rates'

OUTPUT_FILENAME = f'{NAME}.csv'
WRITE_DIR = constants.PIPELINE_OUTPUTS_DIR

TOLERANCE_INTERVAL = [0.02, 1]


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
            'route_ids': {
                x for x in x[2]
                # if x in routes
            },
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

    # key: stop_id
    stops_map = {
        x[0]: (x[1], x[2], x[3], x[4], x[5])
        for x in stops_df.to_numpy()
    }

    # key: route_id
    apc_map = {
        x[0]: (x[1], x[2], x[3])
        for x in apc_df.to_numpy()
    }

    # key: stop_id
    r_final_map = dict()

    for row in routes_df.to_numpy():
        route, stops = (row[0], list(row[1]))

        stops = [x for x in stops if x in stops_map]
        if not stops:
            continue  # This only happens for 1 of the 155 routes

        m_hat = apc_map[route][2]  # target overall rate
        o = np.array([])  # observed orca counts
        p = np.array([])  # tract populations

        for stop in stops:
            o_i, p_i = (stops_map[stop][0], stops_map[stop][3])
            o = np.append(o, o_i)
            p = np.append(p, p_i)

        m = np.sum(o) / np.sum(p)
        c = m_hat / m
        o_hat = c * o

        for i, stop in enumerate(stops):
            r = o_hat[i] / p[i]

            r_final_map[stop] = np.average([r_final_map[stop], r]) \
                if stop in r_final_map else r

    result = []
    for row in stops_df.to_numpy():
        stop_id = row[0]
        tract_num = row[3]
        r_initial = row[5]
        r_final = r_final_map[stop_id]

        if not TOLERANCE_INTERVAL[0] < r_final < TOLERANCE_INTERVAL[1]:
            r_final = r_initial  # backoff if not within tolerance

        result.append([stop_id, tract_num, r_initial, r_final])

    cols = ['stop_id', 'tract_num', 'r_initial', 'r_final']
    return pd.DataFrame(result, columns=cols)


def run_pipeline():
    """
    Aggregates the APC and predicted ORCA rates by known routes.
    """

    # Run pipeline
    stops_df, routes_df, apc_df = load_input()
    stops_df = attach_r_initial(stops_df, apc_df)
    stops_df = attach_r_final(stops_df, routes_df, apc_df)

    print(stops_df)
    print(routes_df)
    print(apc_df)

    # # Write to CSV
    # if not os.path.exists(WRITE_DIR):
    #     os.mkdir(WRITE_DIR)
    # fpath = os.path.join(WRITE_DIR, OUTPUT_FILENAME)
    # df.to_csv(fpath, index=False)
    # print(f'Wrote {OUTPUT_FILENAME} to {WRITE_DIR}')


if __name__ == '__main__':
    run_pipeline()
