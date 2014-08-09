from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    name = StringField('name')
    email = StringField('email')
    password = PasswordField('password')
    remember_me = BooleanField(default=False)


class SignInForm(Form):
    email = StringField('email')
    password = PasswordField('password')
    remember_me = BooleanField(default=False)


class ChannelSearchForm(Form):
    name = StringField('name')


class ChannelAddForm(Form):
    name = StringField('name')
