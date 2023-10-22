from flask import Blueprint, redirect, url_for, session, jsonify
from config import App_Config

auth = Blueprint('google', __name__)

from run import oauth

google = oauth.remote_app(
    'google',
    consumer_key=App_Config.GOOGLE_CLIENT_ID,
    consumer_secret=App_Config.GOOGLE_CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@oauth.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@auth.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({'data': me.data})
    return 'Hello! Log in with your Google account: <a href="/login">Log in</a>'

@auth.route('/login')
def login():
    return google.authorize(callback=url_for('google.authorized', _external=True))

@auth.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Login failed.'

    session['google_token'] = (response['access_token'], '')
    me = google.get('userinfo')
    # Here, 'me.data' contains user information.
    # You can perform a registration process using this information if needed.

    return redirect(url_for('google.index'))

@auth.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('google.index'))
