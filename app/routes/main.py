from app.extensions import db, jwt
from argon2 import PasswordHasher
from flask import request, render_template, redirect, url_for, flash, make_response, session
from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import jwt_required, set_access_cookies, set_refresh_cookies
from sqlalchemy import text
from app.models import User
import sqlalchemy
from app.extensions import client
from datetime import timedelta


main = Blueprint("main", __name__)


# ФУНКЦИЯ ПОЛУЧЕНИЯ ЮЗЕРНЕЙМА ИЛИ ПРИСВОЕНИЯ КЛЕЙМА ГОСТЯ
def get_user():
    verify_jwt_in_request(optional=True)
    jwt_username = get_jwt_identity()
    return jwt_username


# МЕНЕДЖЕР render_template
# УЛУЧШАЕТ И УПРОЩАЕТ ИСПОЛЬЗОВАНИЕ "render_template"
def renTemp_manager(html_name, **variable):
    context = {}

    for key, value in variable.items():
            context[key] = value
    return render_template(f"{html_name}", context=context, client_username = get_user())



@main.route('/', methods = ["GET", "POST"])
def index():

    return renTemp_manager("MainPage.html")

@main.route("/search/<search_request>")
def search(search_request):

    return renTemp_manager("search.html", search_request = search_request)


@main.route("/profile/<string:username>")
def profile(username):


    # ПРОВЕРКА НА СУЩЕСТВОВАНИЕ ПОЛЬЗОВАТЕЛЯ ВЛАДЕЮЩЕГО ПОСЕЩАЕМЫМ ПРОФИЛЕМ
    try: 
        user_exist_check = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()

    except sqlalchemy.exc.NoResultFound:

        return render_template("error404.html")

    


    # ПРОВЕРКА СТАТУСА КЛИЕНТА (ПОСЕТИТЕЛЬ ИЛИ ВЛАДЕЛЕЦ ПРОФИЛЯ)
    status = "guest"
    client_username = get_user()
    if client_username == username:
        status = "admin"
    else:
        status = "guest"

    return renTemp_manager("profile.html", status = status, username=username)

@main.route("/upload_video")
@jwt_required()
def upload_video():
    csrf_token = request.cookies.get('csrf_access_token')
    return render_template("upload_video.html", csrf_token = csrf_token)

@main.route("/profile/None")
def profile_redirect_None():

    return redirect(url_for("auth.login"))

@main.route("/profile/Guest")
def profile_redirect_Guest():

    return redirect(url_for("main.login"))

@main.route("/video/<video_name>")
def video(video_name):
    
    url = client.presigned_get_object(
        "videos",
        video_name,
        expires=timedelta(hours=12)
    )


    return render_template("video.html", video_name=video_name, video_url=url)


@main.errorhandler(401)
def unauthorized(e):

    return render_template("error401.html")

@main.errorhandler(404)
def not_found(e):

    return render_template("error404.html")