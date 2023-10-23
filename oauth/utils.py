from functools import wraps
from flask import session, jsonify
from oauth.config import App_Config
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


# Wrapper function to make sure the user is logged in
def login_is_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'You are not logged in'}), 401
        
        if auth_header.startswith("Bearer"):
            token = auth_header.split(" ")[1]
        user = Users.verify_token(token)
        if not user:
            return jsonify({'message': 'Invalid token'}), 401

        return function(user, *args, **kwargs)

    return decorated_function

def generate_verification_token(user_id):
    # Create a serializer with a secret key
    s = Serializer(App_Config.SECRET_KEY)  # Token expires in 1 hour

    # Create the token
    token = s.dumps(user_id)
    return token
