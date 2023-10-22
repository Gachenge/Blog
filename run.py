from flask import Flask
from config import App_Config
from google.routes import auth
from flasgger import Swagger
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.config.from_object(App_Config)

oauth = OAuth(app) 

# Register the Google authentication blueprint
app.register_blueprint(auth)


swagger = Swagger(app)


if __name__ == '__main__':
    app.run(debug=True)
