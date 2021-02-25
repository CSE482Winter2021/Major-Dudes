import os

import pandas as pd

from pipelines.p3_prep_apc import WRITE_DIR as p3_write_dir
from pipelines.p2_aggregate_orca import WRITE_DIR as p2_write_dir
from utils import constants

NAME = 'p4_aggregate_apc'

SEASON = 'winter'
INTERVAL = 'hr'

OUTPUT_FILENAME = f'p4_apc_aggregate_{INTERVAL}_{SEASON}.csv'
WRITE_DIR = constants.PIPELINE_OUTPUTS_DIR


def load_input():
    """
    Load the specified datasets, clean and filter as needed.
    """

    # Load data
    path1 = os.path.join(p3_write_dir, f'p3_apc_{SEASON}_{INTERVAL}.csv.gz')
    path2 = os.path.join(p2_write_dir, 'routes_aggregate.csv')
    apc_df = pd.read_csv(path1, compression='gzip')
    route_df = pd.read_csv(path2)

    # Filter data
    apc_df = apc_df[apc_df['region'] != 'Express']
    apc_df = apc_df[apc_df['orca_total'] > 0]
    apc_df = apc_df[~apc_df['rte'].isin(
        set.difference(
            set(apc_df['rte']),
            set(route_df['route_id']),
        ))
    ]

    apc_df = apc_df.reset_index(drop=True)
    return apc_df


def aggreate_counts(apc_df):
    """
    Aggregates the APC and predicted ORCA counts by routes.
    """

    result = []

    for route in apc_df['rte'].unique():
        rows = apc_df[apc_df['rte'] == route]
        n_apc = int(rows['ons'].sum())
        n_orca = int(rows['orca_total'].sum())
        result += [[route, n_apc, n_orca, n_orca / n_apc]]

    cols = ['route_id', 'n_apc', 'n_orca', 'orca_rate']
    return pd.DataFrame(result, columns=cols)


def run_pipeline():
    """
    Aggregates the APC and predicted ORCA counts by known routes.
    """

    # Run pipeline
    apc_df = load_input()
    apc_df = aggreate_counts(apc_df)

    # Write to CSV
    if not os.path.exists(WRITE_DIR):
        os.mkdir(WRITE_DIR)
    fpath = os.path.join(WRITE_DIR, OUTPUT_FILENAME)
    apc_df.to_csv(fpath, index=False)
    print(f'Wrote {OUTPUT_FILENAME} to {WRITE_DIR}')


if __name__ == '__main__':
    run_pipeline()
