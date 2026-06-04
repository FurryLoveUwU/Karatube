from app.extensions import db, jwt
from argon2 import PasswordHasher
from flask import Flask, request, render_template, redirect, url_for, flash, make_response, session
from flask import Blueprint, jsonify
import flask_jwt_extended
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from app.models import User


main = Blueprint("main", __name__)

def get_user():
    verify_jwt_in_request(optional=True)
    jwt_username = get_jwt_identity()
    return jwt_username

def renTemp_manager(html_name, username=None, status = None, search_request = None):
    return render_template(f"{html_name}", jwt_username = get_user(), username = username, status = status, search_request = search_request)



@main.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":

        search = request.form.get("search")

        connection = db.session.connection()
        connection.execute(text("CREATE EXTENSION pg_trgm;"))
        connection.execute(text("SELECT * FROM videos WHERE to_tsvector('english', title || ' ' || description)@@ plainto_tsquery('english', 'cat video'"))

        return redirect(f"search/{search}")

    return renTemp_manager("MainPage.html") 

@main.route("/search/<search_request>")
def search(search_request):

    return renTemp_manager("search.html", search_request = search_request)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")


        ph = PasswordHasher()
        res=ph.hash(password)
        password_hash = res

        user = User(username=username, email=email, password_hash=password_hash)
        if len(username) <= 3:
            flash("Слишком короткий юзернейм")
            return renTemp_manager("login.html")
        else:
            user = user
        

        db.session.add(user)
        try:
            db.session.commit()
            flash(f"Вы успешно зарегестрировали аккаунт")
        except Exception as e:
            print(f"Ошибка регистрации 57 - {e}")
            flash(f"Ошибка, не удалось зарегестрировать")
    return renTemp_manager("register.html")



@main.route("/login", methods=["GET", "POST"])
def login():
    access_token = None
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = db.session.execute(db.select(User).where(User.username == username)).scalars().first()
        ph = PasswordHasher()
        
        
        try:
            
            ph.verify(user.password_hash, password)

            access_token = create_access_token(identity=username)
            response = make_response(redirect(url_for("main.profile", username=username)))
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=True,
                samesite="Lax"
            )
            flash("Вход успешен")
            return response
        

        except Exception as e:
            flash("Неверный пароль / юзернейм")
            print("error ln 103", e)
        
        


    return renTemp_manager("login.html")


@main.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.login")))
    
    resp.delete_cookie('access_token')
    return resp


@main.route("/profile/<string:username>")
@jwt_required()
def profile(username):


    status = "guest"
    jwt_username = get_user()
    if jwt_username == username:
        status = "admin"
    else:
        pass


    return renTemp_manager("profile.html", username=username, status = status)

@main.route("/upload_video")
@jwt_required()
def upload_video():

    return render_template("upload_video.html")

@main.route("/profile/None")
def profile_redirect():

    return redirect(url_for("main.login"))



@main.errorhandler(401)
def unauthorized(e):

    return render_template("error401.html")