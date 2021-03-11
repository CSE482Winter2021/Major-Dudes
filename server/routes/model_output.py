from flask import Blueprint, request, session

from server.setup import orca_rates
from utils.server_utils import tojson
from server.setup import orca_rates as setup_orca_rates
from server.db.connection import DBConnection
import server.db.config as db_config

model_output_bp = Blueprint('model_output_bp', __name__)
endpoint = 'model_output'


@model_output_bp.route(f'/{endpoint}', methods=['GET'])
def model_output():

    with DBConnection() as conn:
        col = conn.db.get_collection(db_config.COL_NAME)
        model_w = col.find_one({'type': 'model_w'})

        if not model_w:
            print('training model...')
            model, model_w = orca_rates.get_trained_model()
            col.insert_one({
                'type': 'model_w',
                'data': orca_rates.encode(model_w)
            })
            print('done')

        else:
            model_w = orca_rates.decode(model_w['data'])
            model = orca_rates.get_untrained_model()
            model.W = model_w

    gender = request.args.get('gender')
    age = request.args.get('age')
    race = request.args.get('race')
    income = request.args.get('income')
    dis = request.args.get('dis')

    prediction = model.predict([gender, age, race, income, dis])

    return tojson(prediction)



