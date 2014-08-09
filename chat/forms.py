from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms import validators


class SignUpForm(Form):
    name = StringField('name', [validators.Length(min=4, max=20)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=6, max=10),
    ])
    confirm = PasswordField('Repeat Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])
    remember_me = BooleanField(default=False)


class SignInForm(Form):
    email = StringField('email')
    password = PasswordField('password')
    remember_me = BooleanField(default=False)


class ChannelSearchForm(Form):
    name = StringField('name')


class ChannelAddForm(Form):
    name = StringField('name')
