from config import BaseConfig
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
from werkzeug.utils import secure_filename
from app.extensions import client
import uuid


def get_user():
    verify_jwt_in_request(optional=True)
    jwt_username = get_jwt_identity()
    print("DEBUG LINE 15 api")
    print("jwt username api: ", jwt_username)
    return jwt_username


api = Blueprint("api", __name__, url_prefix='/api')

@api.route("/upload", methods=["POST"])
def upload():
    name        = request.form.get("name")
    description = request.form.get("description")
    tags        = request.form.get("tags")
    file        = request.files["file"]

    filename = secure_filename(file.filename)

    ext = filename.split(".")[-1]
    if ext != "mp4":
        flash("Неправильное расширение. Требуеться MP4")
        return render_template("upload_video.html")
    else:
    
        object_name = f"{uuid.uuid4()}.{ext}"

        client.put_object(
            "videos",
            object_name,
            file.stream,
            length=-1,
            part_size=10*1024*1024
        )

        print("dg ln23 apiroutes")
        print(f"{name}\n{description}\n{tags}\n{file}")
        username=get_user()

        return redirect(url_for("main.main"))

