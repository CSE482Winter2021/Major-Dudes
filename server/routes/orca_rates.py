from flask import Blueprint, session

from utils.server_utils import tojson
from server.setup import orca_rates as setup_orca_rates
from server.db.connection import DBConnection
import server.db.config as db_config

orca_rates_bp = Blueprint('orca_rates_bp', __name__)
endpoint = 'orca_rates'


@orca_rates_bp.route(f'/{endpoint}', methods=['GET'])
def orca_rates():

    with DBConnection() as conn:
        col = conn.db.get_collection(db_config.COL_NAME)
        obj = col.find_one({'type': 'by_stop'})
        return tojson(obj['data'])


@orca_rates_bp.route(f'/{endpoint}/<stop_id>', methods=['GET'])
def orca_rates_stop_id(stop_id):

    with DBConnection() as conn:
        col = conn.db.get_collection(db_config.COL_NAME)
        obj = col.find_one({'type': 'by_stop'})
        data = obj['data']

        if stop_id not in data:
            return tojson(-1)

        return tojson(data[stop_id])
