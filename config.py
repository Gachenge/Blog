import os
from dotenv import load_dotenv

load_dotenv(".env")

class App_Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_CLIENT_ID = os.environ.get('CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = 'http://localhost/api/oauth/callback'
