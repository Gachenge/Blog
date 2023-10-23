import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, Blueprint, jsonify, url_for
from google.oauth2 import id_token
from oauth.config import App_Config
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from oauth import db
from oauth.models.users import Users
from oauth.utils import login_is_required

GOOGLE_CLIENT_ID = App_Config.GOOGLE_CLIENT_ID
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secret.json')

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/api/oauth/callback"
)

auth = Blueprint('google', __name__, url_prefix='/api/oauth')

@auth.route("/login")
def login():
    """Login function to allow the user to log in."""
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth.route("/callback")
def callback():
    """Function to accept authorization token and details from Google."""
    # Check if the state matches
    if session.get("state") != request.args.get("state"):
        abort(500)  # State does not match!

    # Fetch Google user information
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Check if 'google_id', 'name', and 'email' are available in id_info
    if all(key in id_info for key in ['sub', 'name', 'email']):
        # Set session values
        session['google_id'] = id_info['sub']
        session['name'] = id_info['name']
        session['email'] = id_info['email']

        # Check if the user already exists in the database
        user = Users.query.filter_by(google_id=session['google_id']).first()
        if user:
            return jsonify({"user": user.name})

        # Create a new user
        new_user = Users(google_id=session['google_id'], name=session['name'], email=session['email'])
        db.session.add(new_user)
        db.session.commit()

        session['profile'] = id_info.get('profile')
    else:
        return jsonify({"Error": "Google user information not available"})

    return redirect(url_for('google.protected_area'))

@auth.route("/logout")
def logout():
    # Get the user based on their session data, or use the user ID stored in the session
    user_id = session.get("user_id")

    if user_id:
        # Mark the user's token as revoked in the database
        user = Users.query.filter_by(id=user_id).first()
        if user:
            user.token = None  # You can set it to None or delete it, depending on your design.

        db.session.commit()

    # Clear the session data
    session.clear()

    return redirect(url_for('google.index'))


@auth.route("/")
def index():
    login_link = f"<a href='{url_for('google.login')}'><button>Login</button></a>"
    protected_link = f"<a href='{url_for('google.protected_area')}'><button>Protected</button></a>"
    return login_link + "<br>" + protected_link

@login_is_required
@auth.route("/protected_area")
def protected_area():
    return f"Hello {session.get('name')}, your email address is: {session.get('email')}! <br/> <a href='{url_for('google.logout')}'><button>Logout</button></a>"
