import os

import pandas as pd
from tqdm import tqdm

from utils import constants

NAME = 'p3_prep_apc'

INTERVALS = [
    '15min',
    '30min',
    'ampm',
    'day',
    'hr',
]
SEASONS = [
    'combined',
    'summer',
    'winter',
]

WRITE_DIR = os.path.join(constants.PIPELINE_OUTPUTS_DIR, 'p3_apc_by_route')


def load_single(interval, season):
    """
    Load train, test, and val data for a single interval/season combination and
    write to disk.
    """

    data_dir = os.path.join(
        constants.DATA_DIR,
        'orca_apc_by_route',
        f'{season}_data',
        interval,
    )
    paths = [
        os.path.join(data_dir, 'test.tsv.gz'),
        os.path.join(data_dir, 'train.tsv.gz'),
        os.path.join(data_dir, 'xval.tsv.gz'),
    ]
    dfs = [pd.read_csv(path, compression='gzip', sep='\t') for path in paths]
    df = pd.concat(dfs)

    # Write to CSV
    if not os.path.exists(WRITE_DIR):
        os.mkdir(WRITE_DIR)

    fname = f'p3_apc_{season}_{interval}.csv.gz'
    fpath = os.path.join(
        WRITE_DIR,
        fname,
    )
    tqdm.write(f'Writing {fname} to {WRITE_DIR}')
    df.to_csv(fpath, compression='gzip', index=False)


def run_pipeline():
    """
    Unzips and aggregates train, test, and xval, from orca_apc_by_route and
    writes to disk.
    """

    # Run pipeline
    pairs = []
    for interval in INTERVALS:
        for season in SEASONS:
            pairs.append((interval, season))

    n = len(pairs)
    for i in tqdm(range(n), desc='Loading data', dynamic_ncols=True):
        interval, season = pairs[i]
        load_single(interval, season)


if __name__ == '__main__':
    run_pipeline()
