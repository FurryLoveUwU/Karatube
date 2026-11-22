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
from app.models import User, video
from werkzeug.utils import secure_filename
from app.extensions import client
import datetime
import uuid


def get_user():
    verify_jwt_in_request(optional=True)
    jwt_username = get_jwt_identity()
    return jwt_username


api = Blueprint("api", __name__, url_prefix='/api')

@api.route("/upload", methods=["POST"])
def upload():
    username    = get_user()
    video_name  = request.form.get("name")
    description = request.form.get("description")
    tags        = request.form.get("tags")    
    file        = request.files["file"]
    date = datetime.date.today()


    filename = secure_filename(file.filename)

    ext = filename.split(".")[-1]
    if ext != "mp4":
        flash("Неправильное расширение. Требуеться MP4")
        return render_template("upload_video.html")
    else:
    
        object_name = f"{uuid.uuid4()}"

        client.put_object(
            "videos",
            object_name,
            file.stream,
            length=-1,
            part_size=10*1024*1024
        )

        

        
        video_to_db = video(username = username, video_name = video_name, description = description, tags = tags, file = object_name, date = date)
        db.session.add(video_to_db)
        db.session.commit()

        return redirect(url_for("main.index"))
