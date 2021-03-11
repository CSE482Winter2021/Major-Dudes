import numpy as np

import json

from utils.constants import DATA_DIR
from scripts.demographcis_modeller import ORCA_Rate_Model
import pipelines.p5_orca_rates as p5


def get_data():
    data = p5.run_pipeline()
    print(data)
    return {str(int(row[0])): row[1] for row in data}


def get_trained_model():
    model = ORCA_Rate_Model(200)
    census_data_dir = f'{DATA_DIR}/census_data/pipeline_output'
    with open(f'{census_data_dir}/samples.json', 'r') as f:
        j = json.load(f)
        X = j[0]
        y = j[1]
    model.train(X, y)
    return model, model.W


def get_untrained_model():
    return ORCA_Rate_Model(200)


def encode(w):
    return json.dumps(w, cls=NumpyEncoder)


def decode(w):
    return json.loads(w)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
