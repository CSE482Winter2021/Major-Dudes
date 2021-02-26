from tqdm import tqdm

import pipelines.p1_orca_by_stop as p1
import pipelines.p2_aggregate_orca as p2
import pipelines.p3_prep_apc as p3
import pipelines.p4_aggregate_apc as p4
import pipelines.p5_orca_rates as p5

PIPELINES = [p1, p2, p3, p4, p5]


def run_all():
    """
    Runs each pipeline sequentially.
    """

    for i, p in enumerate(PIPELINES):
        tqdm.write(f'\nRunning pipeline {p.NAME} ({i + 1}/{len(PIPELINES)})')
        p.run_pipeline()


if __name__ == '__main__':
    run_all()
