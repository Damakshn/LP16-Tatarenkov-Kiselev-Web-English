from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from web_english import db, login_manager


class ServiceMixin:
    """
    Миксин, позволяющий отслеживать создание и изменение других моделей.
    Чтобы колонки миксина добавлялись в конец, объявляем их через declared_attr
    """
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow)

    @declared_attr
    def last_modified(cls):
        return db.Column(db.DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)


class User(UserMixin, db.Model, ServiceMixin):
    USER_ROLE_ADMIN = 0
    USER_ROLE_STUDENT = 1
    USER_ROLE_CONTENTMAKER = 2

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True,
                         nullable=False)
    # хэш генерируется на before_insert
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    is_email_confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.Integer, nullable=False, default=USER_ROLE_STUDENT)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return f"<User {self.username}>"

    def get_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @classmethod
    def verify_token(cls, token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return cls.query.get(id)


class Content(db.Model, ServiceMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    text_en = db.Column(db.Text, unique=True, nullable=False)
    text_ru = db.Column(db.Text, unique=True, nullable=False)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"<Content {self.title}>"


@login_manager.user_loader
def fetch_user(user_id):
    return User.query.get(user_id)


def generate_password_for_new_user(mapper, connection, target):
    target.password = generate_password_hash(target.password)


db.event.listen(User, 'before_insert', generate_password_for_new_user)
