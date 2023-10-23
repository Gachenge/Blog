from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flasgger import Swagger
from oauth.config import App_Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(App_Config)
    db.init_app(app)
    
    from oauth.google.routes import auth

    # Register the Google authentication blueprint
    app.register_blueprint(auth)

    swagger = Swagger(app)

    return app

