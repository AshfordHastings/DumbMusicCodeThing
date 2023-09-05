from .responses import *

from flask import jsonify, make_response

def response_with(response, value=None, errors=None, headers={}):
    result = {}
    if response.get("message") is not None:
        result.update({"message": response.get("message")})
    if value is not None:
        result.update({"value": value})
    if errors is not None:
        result.update({"error": errors})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)