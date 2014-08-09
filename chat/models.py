from . import db

from flask import url_for
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True,
                     index=True)
    password = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True, index=True)
    messages = db.relationship('Message', backref='user')

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __unicode__(self):
        return self.name

    def check_password(self, password):
        return self.password == password


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False, index=True)
    messages = db.relationship('Message', backref='channel')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return url_for('channel', channel_id=self.id)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column('text', db.Text(200), index=True)

    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user, text, channel_id):
        self.user_id = user.id
        self.text = text
        self.channel_id = channel_id

    def __repr__(self):
        return '<Message %r, %r, %r' % (self.user, self.text, self.channel_id)
