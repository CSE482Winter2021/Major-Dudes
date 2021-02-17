from tqdm import tqdm

import pipelines.p1_xy_to_stop as p1
import pipelines.p2_prep_apc as p2
import pipelines.p3_aggregate_apc as p3

PIPELINES = [p1, p2, p3]


def run_all():
    """
    Runs each pipeline sequentially.
    """

    for i, p in enumerate(PIPELINES):
        tqdm.write(f'\nRunning pipeline {p.NAME} ({i + 1}/{len(PIPELINES)})')
        p.run_pipeline()


if __name__ == '__main__':
    run_all()
