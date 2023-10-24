from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flasgger import Swagger
from oauth.config import App_Config
from flask_github import GitHub


db = SQLAlchemy()
github = GitHub()


def create_app():
    app = Flask(__name__)
    app.config.from_object(App_Config)
    db.init_app(app)
    github.init_app(app)
    
    from oauth.google.routes import auth
    from oauth.github.routes import gh

    # Register the Google authentication blueprint
    app.register_blueprint(auth)
    app.register_blueprint(gh)

    swagger = Swagger(app)

    return app

