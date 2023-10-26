from functools import wraps
from flask import session, jsonify, request
from oauth.config import App_Config
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import jwt


# Wrapper function to make sure the user is logged in
def login_is_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')

        if jwt_token:
            if jwt_token.startswith("Bearer"):
                token = jwt_token.split(' ')[1]
                try:
                    user_id = verify_verification_token(token)
                    if user_id:
                        return function(user_id, *args, **kwargs)
                    else:
                        return jsonify({"error": "Token is invalid"}), 401
                except jwt.ExpiredSignatureError:
                    return jsonify({"error": "Token has expired"}), 401
                except jwt.DecodeError:
                    return jsonify({"error": "Token is invalid"}), 401
        else:
            return jsonify({"error": "You are not logged in"}), 401

    return decorated_function


def generate_verification_token(user_id):
    # Create a serializer with a secret key and an expiration time (in seconds)
    s = Serializer(App_Config.SECRET_KEY)  # Token expires in 1 hour

    # Create the token
    token = s.dumps({'user_id': user_id})
    return token


def verify_verification_token(token):
    s = Serializer(App_Config.SECRET_KEY)

    try:
        # Deserialize the token and extract the user_id
        data = s.loads(token)
        user_id = data.get('user_id')
        return user_id
    except Exception as e:
        # Token is invalid or has expired
        return None
