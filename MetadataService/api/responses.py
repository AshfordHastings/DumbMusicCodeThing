from flask import make_response, jsonify

SUCCESS_200 = {
    "http_code": 200,
    'message': 'success'
}

SUCCESS_201 = {
    "http_code": 201,
    'message': 'success'
}

SUCCESS_204 = {
    "http_code": 204,
    'message': 'success'
}

ERROR_401 = {
    "http_code": 204,
    'message': 'success'
}

ERROR_500 = {
    "http_code": 500,
    'message': 'error'
}

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