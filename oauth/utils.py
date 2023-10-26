from functools import wraps
from flask import session, jsonify
from oauth.config import App_Config
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


# Wrapper function to make sure the user is logged in
def login_is_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        jwt_token = session.get('jwt_token')
        if jwt_token:
            try:
                user_id = verify_verification_token(jwt_token)
                return function(user_id, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"Error": "Token is expired"})
            except jwt.DecodeError:
                return jsonify({"Error": "Token is invalid"})
            except Exception as e:
                return jsonify({"Error": "Verification failed"})
        else:
            return jsonify({"Error": "You are not logged in"})
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
