from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

if not client.bucket_exists("videos"):
    client.make_bucket("videos")



db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db)
jwt = JWTManager()