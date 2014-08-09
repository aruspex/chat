from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms import validators

from .models import User


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

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data,
        ).first()

        if user is None:
            self.email.errors.append('Unregistered email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ChannelSearchForm(Form):
    name = StringField('name')


class ChannelAddForm(Form):
    name = StringField('name')
