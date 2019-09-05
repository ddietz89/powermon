from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error(status, message=None):
    data = {'error': HTTP_STATUS_CODES.get(status, 'Unknown')}
    if message:
        data['message'] = message

    response = jsonify(data)
    response.status_code = status

    return response

def bad_post(message):
    return error(414, message)
