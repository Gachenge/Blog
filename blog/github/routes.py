from flask import Blueprint, redirect, url_for, jsonify, session
from flask_dance.contrib.github import make_github_blueprint, github
from blog.config import App_Config
from blog.models.users import Users
from blog import db
from blog.utils import generate_verification_token, login_is_required


github_bp = make_github_blueprint(client_id=App_Config.GITHUB_OAUTH_CLIENT_ID,
                                  client_secret=App_Config.
                                  GITHUB_OAUTH_CLIENT_SECRET)


@github_bp.route('/')
def github_login():
    """
    Allow users to log in via GitHub OAuth.
    If the user is authorized, their GitHub details
    (name and email) are saved to the database.
    Responses:
        200:
            - Success: New user created (if the user is
            successfully authenticated and added to the database).
        401:
            - Error: GitHub account not found (if the GitHub
            account could not be authenticated).
    Returns:
        - A JSON response indicating success or failure.
        - If successful, a new user is created, or the user is
        authenticated and logged in.
    """
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            user = Users.query.\
                filter_by(email=account_info_json['email']).first()
            if not user:
                user = Users(account_id=account_info_json['id'],
                             name=account_info_json['name'],
                             email=account_info_json['email'],
                             avatar=account_info_json['avatar_url'],
                             token=None)
                db.session.add(user)
                db.session.commit()
            jwt_token = generate_verification_token(user.id)
            user.token = jwt_token
            db.session.commit()
        return redirect(url_for('google.protected_area'))
    return ({"Error": "User not authorised"}), 401
