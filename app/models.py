from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}'.format(self.name)

    def __str__(self):
        return 'Role: {} --- {}'.format(self.id, self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    document = db.relationship('Document', backref='user')

    # json field? - дополнительные сопутствующие поля если нужно

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return 'User: {} --- {}'.format(self.id, self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256), unique=True)
    url = db.Column(db.String(2048))
    is_active = db.Column(db.Boolean, default=True)
    documents = db.relationship('Document', backref='source')

    def __repr__(self):
        return '<Source {}>'.format(self.name)

    def __str__(self):
        return 'Source: {} --- {}'.format(self.id, self.name)


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024), unique=True)
    text = db.Column(db.Text())
    url = db.Column(db.String(2048))  # TODO need url validator
    created = db.Column(db.DateTime)
    added = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow())
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
