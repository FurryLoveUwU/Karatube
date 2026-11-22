from app.extensions import db, jwt
from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for
from argon2 import PasswordHasher
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, set_access_cookies, set_refresh_cookies, create_refresh_token, create_access_token, jwt_required
from app.models import User
import sqlalchemy
import re

auth = Blueprint("auth", __name__)




def get_user():
    verify_jwt_in_request(optional=True)
    jwt_username = get_jwt_identity()
    return jwt_username

def renTemp_manager(html_name, **variable):
    context = {}

    for key, value in variable.items():
            context[key] = value
    return render_template(f"{html_name}", context=context, client_username = get_user())




@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        # НАЗНАЧЕНИЕ ПЕРЕМЕННЫХ
        username = request.form.get("username")
        username = username.lower()
        email = request.form.get("email")
        password = request.form.get("password")
        

        # ПРОВЕРКА
        check_status = True
        if re.search(r"[^'0-9a-zA-Z_']", username) == None:
            pass
        else:
            check_status = False
            flash("Username uses wrong symbols")
            

        if re.search(r"[^'0-9a-zA-Z.@']", email) == None:
            pass
        else:
            flash("email uses wrong symbols")
            check_status = False

        if re.search(r"[^'0-9a-zA-Z!@#$%^&*()_']", password) == None:
            pass
        else:
            flash("Password uses wrong symbols")
            check_status = False


        # ФИНАЛЬНОЕ ДОБАВЛЕНИЕ В БД
        if check_status != False:
            ph = PasswordHasher()
            password_hash=ph.hash(password)
            user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            try:
                db.session.commit()
                flash(f"Вы успешно зарегестрировали аккаунт")

            except sqlalchemy.exc.IntegrityError:
                flash("Такой юзернейм/почта уже существует")

            except Exception as e:
                print(f"Ошибка регистрации 79ln - {e}")
                flash(f"Произошла неизвестная ошибка")
        else:
            pass
    return renTemp_manager("register.html")



@auth.route("/login", methods=["GET", "POST"])
def login():
    access_token = None
    if request.method == "POST":

        username = request.form.get("username")
        username = username.lower()
        password = request.form.get("password")

        user = db.session.execute(db.select(User).where(User.username == username)).scalars().first()
        ph = PasswordHasher()
        
        
        try:
            
            ph.verify(user.password_hash, password)

            access_token  = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = make_response(redirect(url_for("main.profile", username=username)))
            set_refresh_cookies(response, refresh_token)
            set_access_cookies(response, access_token)

            flash("Вход успешен")
            return response
        

        except Exception as e:
            flash("Неверный пароль / юзернейм")
            print("error ln 89 login", e)
        
        
    return renTemp_manager("login.html")


@auth.route("/logout")
def logout():

    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie('access_token')
    resp.delete_cookie('refresh_token_cookie')
    resp.delete_cookie('csrf_access_token')
    resp.delete_cookie('csrf_refresh_token')
    return resp



@auth.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()

    access_token = create_access_token(identity=identity)

    refresh_token = create_refresh_token(identity=identity)

    response = make_response(redirect(url_for("main.index", username=get_user())))

    set_refresh_cookies(response, refresh_token)
    set_access_cookies(response, access_token)

    return response