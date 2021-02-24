import os

import pandas as pd
from tqdm import tqdm

import pipelines.p1_orca_by_stop as p1
from utils import constants, data_utils

NAME = 'p2_aggregate_orca'

WRITE_DIR = os.path.join(constants.PIPELINE_OUTPUTS_DIR, NAME)


def load_input():
    path = os.path.join(constants.PIPELINE_OUTPUTS_DIR, f'{p1.NAME}.csv')
    return pd.read_csv(path)


def aggregate_stops(orca_df):
    """
    Aggregates the ORCA dataset by summing together the boardings at each stop.
    """

    cols = [
        'stop_id',
        'boarding_count',
        'route_ids',
        'tract_num',
        'tract_population'
    ]
    stops = orca_df['stop_id'].unique()
    result = []

    for stop in tqdm(stops, desc='Aggregating stops'):
        rows = orca_df[orca_df[cols[0]] == stop]
        result.append([
            stop,
            rows[cols[1]].sum(),
            rows[cols[2]].iloc[0],
            rows[cols[3]].iloc[0],
            rows[cols[4]].iloc[0],
        ])

    return pd.DataFrame(result, columns=cols)


def aggregate_routes(orca_df):
    """
    Maps each route to its list of stops.
    """

    routes = {}
    for row in orca_df.to_numpy():
        stop_id = row[0]
        route_ids = data_utils.parse_collection(row[2], set, int)

        for route_id in route_ids:
            routes.setdefault(route_id, set()).add(stop_id)

    cols = ['route_id', 'stop_ids']
    result = [[route_id, routes[route_id]] for route_id in routes]
    return pd.DataFrame(result, columns=cols)


def run_pipeline():
    """
    Runs the pipeline and writes the outputs to disk.
    """

    orca_df = load_input()
    orca_df = aggregate_stops(orca_df)
    routes_df = aggregate_routes(orca_df)

    # Write to CSV
    if not os.path.exists(WRITE_DIR):
        os.mkdir(WRITE_DIR)
    files = {'stops_aggregate.csv': orca_df, 'routes_aggregate.csv': routes_df}
    for fname in files:
        files[fname].to_csv(os.path.join(WRITE_DIR, fname), index=False)
        tqdm.write(f'Wrote {fname} to {WRITE_DIR}')


if __name__ == '__main__':
    run_pipeline()
