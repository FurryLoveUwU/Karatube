from flask_login import (LoginManager, UserMixin, login_required, login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy import CheckConstraint

def load_user(user_id):
    from app.models import User
    res = User.get(user_id)
    return res



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(12), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<id:{}:username:{}>".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user(user_id):
        user = db.one_or_404(db.select(User).filter_by(id=user_id))
        return user

    __table_args__ = (
        CheckConstraint("length(trim(email)) > 0", name="email_not_empty"),
        CheckConstraint("length(trim(username)) > 0", name="username_not_empty"),
        CheckConstraint("length(trim(username)) < 3", name="username_too_short"),
    )

class video(db.Model):
    __tablename__ = "video"

    id = db.Column(db.Integer(), primary_key = True)
    username    = db.Column(db.String(20),    nullable=False)
    video_name  = db.Column(db.String(50),    nullable=False)
    description = db.Column(db.String(1024),  nullable=False)
    tags        = db.Column(db.String(1024),  nullable=False)
    date        = db.Column(db.String(1024),  nullable=False)
    file        = db.Column(db.String(1024),  nullable=False)


    def __repr__(self):
        return "<id:{}:username:{}>".format(self.id, self.username)