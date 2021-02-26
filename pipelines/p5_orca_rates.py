import os

import pandas as pd

from pipelines.p2_aggregate_orca import WRITE_DIR as p2_write_dir
from pipelines.p4_aggregate_apc import WRITE_DIR as p4_write_dir
from pipelines.p4_aggregate_apc import OUTPUT_FILENAME as p4_fname
from utils import constants, data_utils

NAME = 'p5_orca_rates'

OUTPUT_FILENAME = f'{NAME}.csv'
WRITE_DIR = constants.PIPELINE_OUTPUTS_DIR


def load_input():
    """
    Load the specified datasets.
    """

    # Load data
    path1 = os.path.join(p2_write_dir, 'routes_aggregate.csv')
    path2 = os.path.join(p2_write_dir, 'stops_aggregate.csv')
    path3 = os.path.join(p4_write_dir, p4_fname)
    routes_df = pd.read_csv(path1)
    stops_df = pd.read_csv(path2)
    apc_df = pd.read_csv(path3)

    return routes_df, stops_df, apc_df


def run_pipeline():
    """
    Aggregates the APC and predicted ORCA counts by known routes.
    """

    # Run pipeline
    routes_df, stops_df, apc_df = load_input()

    # # Write to CSV
    # if not os.path.exists(WRITE_DIR):
    #     os.mkdir(WRITE_DIR)
    # fpath = os.path.join(WRITE_DIR, OUTPUT_FILENAME)
    # df.to_csv(fpath, index=False)
    # print(f'Wrote {OUTPUT_FILENAME} to {WRITE_DIR}')


if __name__ == '__main__':
    run_pipeline()
