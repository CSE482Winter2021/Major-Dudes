import os


class BaseConfig:
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = 'dev'
    SESSION_TYPE = 'filesystem'


API_HOST = '0.0.0.0'
API_PORT = os.environ.get('PORT', 5000)
