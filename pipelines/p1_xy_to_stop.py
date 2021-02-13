import pandas as pd
import numpy as np
import sklearn.neighbors as knn
import os

from utils import constants


# Parameters
KNN_LEAF_SIZE = 50


def _print_unique(df):
    for col in df:
        u = df[col].unique()
        print(f'{col}: {len(df[col])}, {len(u)} unique')
        print(u)
        print()


def _load_inputs():
    """
    Load orca->xy and xy->stops datasets, filter for values we care about.
    """

    # Load data
    path1 = os.path.join(constants.DATA_DIR, 'orca_by_xy.csv')
    path2 = os.path.join(constants.DATA_DIR, 'stops_to_xy.csv')
    orca_df = pd.read_csv(path1)
    stop_df = pd.read_csv(path2)

    # Clean and filter
    orca_df = orca_df[orca_df['boarding_longitude'].notnull()]
    orca_df = orca_df[orca_df['boarding_latitude'].notnull()]

    orca_df = orca_df[orca_df['boarding_type'] != 'Transfer']
    orca_df = orca_df[orca_df['mode_abbrev'] == 'Bus']
    orca_df = orca_df[orca_df['agency'] == 'KCM']

    stop_df = stop_df[stop_df['source_agency_id'] == 4]

    orca_df = orca_df.reset_index(drop=True)
    stop_df = stop_df.reset_index(drop=True)
    return orca_df, stop_df


def _reduce_stop_df(stop_df):
    """
    Aggregate stop_df to only include unique stop IDs by averaging the xy
    coordinates of duplicates.
    """

    return stop_df


def _map_nearest_neighbors(orca_df, stop_df):
    """
    Find the stop ID and route number for each entry in orca_df by the nearest
    xy pair in stop_df.
    """

    # Get knn tree
    def get_pair(s_row):
        return (float(s_row['lat']), float(s_row['lon']))

    x = [get_pair(stop_df.iloc[i]) for i in range(stop_df.shape[0])]
    tree = knn.KDTree(x, leaf_size=KNN_LEAF_SIZE)

    # Run 1nn over dataset
    n = orca_df.shape[0]
    for i in range(n):

        # TODO implement reference table for duplicate xy pairs

        # Query knn tree
        o_row = orca_df.iloc[i]
        o_lat = o_row['boarding_latitude']
        o_lon = o_row['boarding_longitude']
        x_i = np.array([o_lat, o_lon]).reshape((1, -1))

        dist, nn_index = tree.query(x_i, k=1)
        nn_index = nn_index[0]  # unpack single value

        s_row = stop_df.iloc[nn_index]
        s_lat = float(s_row['lat'])
        s_lon = float(s_row['lon'])

        if i % (n / 100) == 0:
            print(
                f'{i} / {orca_df.shape[0]}\t'
                f'({round(100 * i / n, 2)}%)'
            )


def run_pipeline():
    """
    Creates a mapping from each entry in winter 2019 ORCA dataset to its
    associated stop ID and route number.
    """

    orca_df, stop_df = _load_inputs()
    print('Done loading')

    # stop_df = _reduce_stop_df(stop_df)
    # print('Done reducing')

    # _map_nearest_neighbors(orca_df, stop_df)
    # print('Done mapping')

    print('ORCA_DF')
    _print_unique(orca_df)

    print('STOP_DF')
    _print_unique(stop_df)


if __name__ == '__main__':
    run_pipeline()
