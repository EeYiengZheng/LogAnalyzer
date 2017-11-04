import datetime

from app import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash, hashlib


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    logs = db.relationship('Log', backref='owner', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return str(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.email)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    internal_f_name = db.Column(db.String(128), unique=True)
    file_hash = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Log %r by %r>' % (self.filename, self.user_id)
