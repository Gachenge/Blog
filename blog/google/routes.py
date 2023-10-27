import os
import pathlib
import requests
from flask import session, redirect, request, Blueprint, jsonify, url_for
from google.oauth2 import id_token
from oauth.config import App_Config
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from oauth import db
from oauth.models.users import Users
from oauth.utils import (login_is_required, generate_verification_token,
                         verify_verification_token)


GOOGLE_CLIENT_ID = App_Config.GOOGLE_CLIENT_ID
client_secrets_file = os.path.join(pathlib.Path(__file__).parent,
                                   'client_secret.json')

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/api/google/callback"
)

auth = Blueprint('google', __name__, url_prefix='/api/google')


@auth.route("/login")
def login():
    """Login function to allow the user to log in using Google OAuth.
    Redirects the user to Google's login page to authenticate.
    Returns:
        Redirects the user to Google's login page for authentication.
    """
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth.route("/callback")
def callback():
    """Function to accept authorization token and details from Google.
    This function handles the callback from Google OAuth. It verifies
    the authorization token and extracts user details.
    Returns:
        - If successful, redirects to the protected area.
        - If unsuccessful, returns a JSON response with an error message.
    """
    # Check if the state matches
    if session.get("state") != request.args.get("state"):
        abort(500)  # State does not match!

    # Fetch Google user information
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.\
        requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # Check if 'google_id', 'name', and 'email' are available in id_info
    if all(key in id_info for key in ['sub', 'name', 'email']):

        # Check if the user already exists in the database
        user = Users.query.filter_by(email=id_info['email']).first()

        if user is None:
            # Create a new user
            user = Users(account_id=id_info['sub'], name=id_info['name'],
                         email=id_info['email'], avatar=id_info['picture'],
                         token=None)
            db.session.add(user)
            db.session.commit()

        session['profile'] = id_info.get('profile')

        # Generate a JWT token and store it in the user's session
        jwt_token = generate_verification_token(user.id)
        user.token = jwt_token
        db.session.commit()

        return redirect(url_for('google.protected_area'))
    else:
        return jsonify({"Error": "Google user information not available"})


@auth.route("/logout")
@login_is_required
def logout(user_id):
    """Logout the user by clearing the session data.
    Clears the user's session data, including the JWT token,
    to log the user out.
    Returns:
        Redirects the user to the index page after logging out.
    """
    # clear session data
    session.clear()

    # remove the token from the user's record
    user = Users.query.filter_by(id=user_id).first()
    if user:
        user.token = None
        db.session.commit()

    return jsonify({"Success": "You have been logged out"})


@auth.route("/")
def index():
    """Render the index page with login options.
    Displays buttons to log in with Google and GitHub
    and access the protected area.
    Returns:
        HTML page with login options.
    """
    google_link = f"<a href='{url_for('google.login')}'><button>Login with google</button></a>"
    github_link = f"<a href='{url_for('github.github_login')}'><button>Login with github</button></a>"
    protected_link = f"<a href='{url_for('google.protected_area')}'><button>Protected</button></a>"
    return google_link + "<br>" + github_link + "<br>" + protected_link


@auth.route("/protected_area")
@login_is_required
def protected_area():
    """Protected area accessible to logged-in users.
    Displays the protected area with the user's name
    and email. Allows the user to log out.
    Returns:
        - If the user is logged in, displays user
        details and a logout button.
        - If the user is not logged in or if the user is not found,
        returns an error message.
    """
    jwt_token = request.headers.get('Authorization')
    token = jwt_token.split(' ')[1]
    user_id = verify_verification_token(token)
    user = Users.query.filter_by(id=user_id).first()
    if user:
        return f"Hello {user.avatar}, {user.name}, your email address is: {user.email}!<a href='{url_for('google.logout')}'><button>Logout</button></a>"
    else:
        return jsonify({"Error": "User not found or you are not\
                        logged in"}), 400
