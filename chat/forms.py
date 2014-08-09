from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms import validators

from .models import User


class UserDataMixin(object):

    def get_user_data(self):
        self.user_data = self.data
        self.rmmbrme = self.user_data.pop('remember_me')


class SignUpForm(Form, UserDataMixin):
    name = StringField('name', [validators.Length(min=4, max=20)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=6, max=10),
    ])
    confirm = PasswordField('Repeat Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])
    remember_me = BooleanField(default=False)

    def validate(self):
        self.get_user_data()
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.name == self.name.data).first()
        if user:
            self.name.errors.append('This user already exist')
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user:
            self.email.errors.append('User with this email already exist')
            return False
        return True

    def get_user_data(self):
        super(SignUpForm, self).get_user_data()
        self.user_data.pop('confirm')


class SignInForm(Form, UserDataMixin):
    email = StringField('email')
    password = PasswordField('password')
    remember_me = BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        self.get_user_data()
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
