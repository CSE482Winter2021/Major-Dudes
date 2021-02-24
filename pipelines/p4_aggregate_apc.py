import os

import pandas as pd

from pipelines.p3_prep_apc import WRITE_DIR as p3_write_dir
from utils import constants, data_utils

NAME = 'p3_aggregate_apc.py'

SEASON = 'winter'
INTERVAL = 'hr'

OUTPUT_FILENAME = f'p3_apc_{INTERVAL}_{SEASON}.csv'
WRITE_DIR = constants.PIPELINE_OUTPUTS_DIR


def load_input():
    """
    Load the specified dataset, clean and filter as needed.
    """

    # Load data
    path = os.path.join(p3_write_dir, f'p3_apc_{SEASON}_{INTERVAL}.csv.gz')
    apc_df = pd.read_csv(path, compression='gzip')
    data_utils.print_unique(apc_df)

    return apc_df


def run_pipeline():
    """
    Creates a mapping from each entry in winter 2019 ORCA dataset to its
    associated stop ID and route number and writes this mapping to disk.
    """

    # Run pipeline
    apc_df = load_input()
    print(apc_df)


if __name__ == '__main__':
    run_pipeline()
