from flask import Flask, redirect, url_for, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from config import DevelopementConfig
from app.routes import mainRoutes
from app.routes.mainRoutes import main
from app.routes.apiRoutes import api
from app.models import User
from app.extensions import db, jwt
import psycopg2



app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(api)

app.config.from_object(DevelopementConfig)

db.init_app(app)


conn_string = "host='localhost' dbname='flask_db' user='postgres' password='3678'"
conn = psycopg2.connect(conn_string)

@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for("main.login"))

@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):

    resp = make_response(redirect(url_for("main.login")))
    resp.set_cookie('access_token', '') 
    return resp



jwt.init_app(app)

with app.app_context():
    db.create_all()

