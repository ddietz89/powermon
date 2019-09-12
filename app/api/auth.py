from flask import g
from flask_httpauth import HTTPTokenAuth
from flask_login import current_user
from app.auth.models import User
from app.api.errors import error

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    if token:
        g.current_user = User.check_token(token)
    else:
        if current_user and current_user.is_authenticated:
            g.current_user = current_user
	else:
	    g.current_user = None

    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error(401)
