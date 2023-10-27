from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from blog.config import App_Config
from flask_dance.contrib.github import make_github_blueprint, github
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(App_Config)
    db.init_app(app)

    from blog.google.routes import auth
    from blog.github.routes import github_bp
    from blog.users.routes import user_bp
    from blog.posts.routes import posts_bp
    from blog.comments.routes import comment_bp

    # Register the blueprint
    app.register_blueprint(auth)
    app.register_blueprint(github_bp, url_prefix='/api/github')
    app.register_blueprint(user_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comment_bp)

    # Initialize CORS
    CORS(app, supports_credentials=True)

    #configure swagger UI
    SWAGGER_URL = '/api/apidocs'
    API_URL = '/swagger.json'
    swagerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "authentications"
        }
    )

    @app.route('/swagger.json')
    def swagger():
        with open('swagger.json', 'r') as f:
            return jsonify(json.load(f))

    app.register_blueprint(swagerui_blueprint, url_prefix=SWAGGER_URL)

    return app
