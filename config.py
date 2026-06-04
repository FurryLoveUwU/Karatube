import os
from dotenv import load_dotenv


load_dotenv()

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SthKFDMsds;gkfF2@!!fdspldaf#rF'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'FOEOUSFGkbhbghlkhrsdjlnkjUI4IUGHKBK,Bnkb'
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token"

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    ALLOWED_EXTENSIONS = {"png", "mp4"}

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopementConfig(BaseConfig):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///database.db'

    