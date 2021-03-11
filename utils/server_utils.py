from flask import make_response
import json


def tojson(res):
    r = make_response(json.dumps(res, default=str))
    r.mimetype = 'application/json'
    return r
