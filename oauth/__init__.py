from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flasgger import Swagger
from oauth.config import App_Config
from flask_dance.contrib.github import make_github_blueprint, github


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(App_Config)
    db.init_app(app)
    
    from oauth.google.routes import auth
    from oauth.github.routes import github_bp

    # Register the blueprint
    app.register_blueprint(auth)
    app.register_blueprint(github_bp, url_prefix='/api/github')

    swagger = Swagger(app)

    return app
