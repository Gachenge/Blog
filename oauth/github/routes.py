from flask import Blueprint, url_for
from oauth import github


gh = Blueprint('github', __name__, url_prefix='/api/github')

@gh.route('/login')
def login():
    return github.authorize()

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

@gh.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('google.index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.github_access_token = oauth_token
    db_session.commit()
    return redirect(next_url)
