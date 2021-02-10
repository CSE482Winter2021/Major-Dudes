import pandas as pd
import numpy as np
import os

from utils import constants


def _print_unique(df):
    for col in df:
        u = df[col].unique()
        print(f'{col}: {len(df[col])}, {len(u)} unique')
        print(u)
        print()


def load_inputs():

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


def get_1nn(orca_df, stop_df, orca_idx):
    o_row = orca_df.iloc[orca_idx]
    o_lat = o_row['boarding_latitude']
    o_lon = o_row['boarding_longitude']

    stop_idx_nn = 0
    dist_nn = np.inf

    def l1_norm(x1, y1, x2, y2):
        return np.abs(np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2])))

    for stop_idx in range(0, stop_df.shape[0]):
        s_row = stop_df.iloc[stop_idx]
        s_lat = s_row['lat']
        s_lon = s_row['lon']

        dist = l1_norm(o_lat, o_lon, s_lat, s_lon)
        if dist < dist_nn:
            dist_nn = dist
            stop_idx_nn = stop_idx

    print(stop_idx_nn)
    print(dist_nn)
    print(stop_df.iloc[stop_idx_nn])
    return stop_idx_nn


def run_pipeline():
    orca_df, stop_df = load_inputs()

    # get_1nn(orca_df, stop_df, 30)

    print('ORCA_DF')
    _print_unique(orca_df)

    print('STOP_DF')
    _print_unique(stop_df)


if __name__ == '__main__':
    run_pipeline()
