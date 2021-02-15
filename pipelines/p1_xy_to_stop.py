import os

import pandas as pd
import numpy as np
import sklearn.neighbors as knn
from tqdm import tqdm

from utils import constants, data_utils


# Parameters
KNN_LEAF_SIZE = 50

OUTPUT_FILENAME = 'p1_orca_by_stop'


def load_inputs():
    """
    Load orca->xy and xy->stops datasets, filter for rows we care about.
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


def reduce_stop_df(stop_df):
    """
    Aggregate stop_df to only include unique stop IDs by averaging the xy
    coordinates of duplicates.
    """

    seen = dict()
    result = []

    n = stop_df.shape[0]
    for i in tqdm(range(n), desc='Reducing stops data'):
        row = stop_df.iloc[i].to_numpy()
        stop_id = int(row[2])

        if stop_id not in seen:
            result.append(row)
            seen[stop_id] = len(result) - 1

        else:
            i_update = seen[stop_id]
            row_update = result[i_update]

            # I haven't seen any cases where the update is different and taking
            # the avg is needed, but let's keep it to be safe.
            lon = np.average([row_update[3], row[3]])
            lat = np.average([row_update[4], row[4]])
            row_update[3] = lon
            row_update[4] = lat

            result[i_update] = row_update

    result_df = pd.DataFrame(result, columns=stop_df.columns)
    return result_df


def map_nearest_neighbors(orca_df, stop_df):
    """
    Find the stop ID and route number for each entry in orca_df by the nearest
    xy pair in stop_df.
    """

    # Get knn tree
    def get_pair(s_row):
        return (float(s_row['lat']), float(s_row['lon']))

    x = [get_pair(stop_df.iloc[i]) for i in range(stop_df.shape[0])]
    tree = knn.KDTree(x, leaf_size=KNN_LEAF_SIZE)

    # Columns:
    # 0 'season', 1 'passenger_type', 2 'boarding_type', 3 'boarding_latitude',
    # 4 'boarding_longitude', 5 'agency', 6 'mode_abbrev', 7 'product_type',
    # 8 'time_period', 9 'day_type', 10 'boarding_count'
    orca_arr = orca_df.to_numpy()
    stop_arr = stop_df.to_numpy()
    ids = []

    # Run 1nn over dataset
    n = len(orca_arr)
    for i in tqdm(range(n), desc='Calculating nearest neighbors'):

        # Query knn tree
        o_row = orca_arr[i]
        o_lat = o_row[3]
        o_lon = o_row[4]
        x_i = np.array([o_lat, o_lon]).reshape((1, -1))

        # TODO some of these distances are really high. Look into it?
        _, nn_index = tree.query(x_i, k=1)
        nn_index = nn_index[0]

        s_row = stop_arr[nn_index][0]
        ids.append((int(s_row[1]), int(s_row[2])))  # route_id, stop_id

    # Merge orca and stop datasets
    merged_arr = []
    for i in tqdm(range(n), desc='Merging datasets'):
        route_id, stop_id = ids[i]
        merged_row = np.copy(orca_arr[i])
        merged_row = np.append(merged_row, route_id)
        merged_row = np.append(merged_row, stop_id)
        merged_arr.append(merged_row)

    cols = np.copy(orca_df.columns)
    cols = np.append(cols, 'route_id')
    cols = np.append(cols, 'stop_id')
    return pd.DataFrame(merged_arr, columns=cols)


def run_pipeline():
    """
    Creates a mapping from each entry in winter 2019 ORCA dataset to its
    associated stop ID and route number and writes this mapping to disk.
    """

    # Run pipeline
    orca_df, stop_df = load_inputs()
    stop_df = reduce_stop_df(stop_df)
    merged_df = map_nearest_neighbors(orca_df, stop_df)

    print('Output:')
    data_utils.print_unique(merged_df)

    # Write CSV
    if not os.path.exists(constants.WRITE_DIR):
        os.mkdir(constants.WRITE_DIR)
    fname = os.path.join(constants.WRITE_DIR, f'{OUTPUT_FILENAME}.csv')
    merged_df.to_csv(fname)
    print(f'Wrote {OUTPUT_FILENAME}.csv to {constants.WRITE_DIR}')


if __name__ == '__main__':
    run_pipeline()
