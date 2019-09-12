from app import db
from werkzeug import generate_password_hash
from datetime import datetime
import jwt
from time import time
from flask import current_app

from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(192), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    removed = db.Column(db.DateTime, default=0)
    last_seen = db.Column(db.DateTime, default=0)

    def __init__(self, name, username, email):
        self.name = name
	self.username = username
	self.email = email

    def set_password(self, password):
        self.datetimemodified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8') 

    def to_dict(self):
        data = {
           'id': self.id,
           'name': self.name,
           'username': self.username,
           'last_seen': self.last_seen,
           'email': self.email,
           'created': self.created,
           'modified': self.modified,
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'username', 'email']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def check_token(token):
        return User.query.filter_by(token=token).first()
