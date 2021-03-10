import pymongo
from collections import OrderedDict

from server.db import config
from server.setup import orca_rates as setup_orca_rates


class DBConnection:
    def __init__(self, host=config.DB_HOST, port=config.DB_PORT):
        self.host = host
        self.port = port
        self.client = None
        self.db = None

    def __enter__(self):

        # Open a DB connection
        url = (
            f'{config.PROTOCOL}://'
            f'{config.DB_USER}:{config.DB_PASS}@'
            f'{config.DB_HOST}:{config.DB_PORT}'
        ) if config.DB_USER and config.DB_PASS else (
            f'{config.PROTOCOL}://'
            f'{config.DB_HOST}:{config.DB_PORT}'
        )
        self.client = pymongo.MongoClient(url)
        self.db = self.client[config.DB_NAME]
        cols = self.db.list_collection_names()

        # Populate database if empty
        if config.COL_NAME not in cols:
            self.db.create_collection(config.COL_NAME)
            col = self.db.get_collection(config.COL_NAME)

            data = setup_orca_rates.get_data()
            col.insert_one({
                'type': 'by_stop',
                'data': data
            })

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
