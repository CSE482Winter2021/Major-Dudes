from flask import Flask, session
from flask_cors import CORS

from utils.server_utils import tojson
import server.config as api_config

from server.routes.orca_rates import orca_rates_bp
from server.routes.model_output import model_output_bp


app = Flask(__name__)
app.config.from_object('config.BaseConfig')
CORS(app)


# GET to the root clears the session cache
@app.route('/', methods=['GET'])
def root():
    session.clear()
    return tojson('Session cleared')


# Attach routes
app.register_blueprint(orca_rates_bp)
app.register_blueprint(model_output_bp)

if __name__ == '__main__':
    app.run(host=api_config.API_HOST, port=api_config.API_PORT)
