from . import app, db, lm
from .forms import SignUpForm, SignInForm, ChannelSearchForm
from .models import Channel, Message, User
from .namespaces import ChatNamespace
from .utils import get_object_or_404, get_or_create

from flask import (
    redirect, render_template, Response,
    request, url_for
)
from flask.views import View
from flask.ext.login import (
    login_required, login_user, logout_user, current_user
)

from socketio import socketio_manage


@lm.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class BaseChatView(View):
    def __init__(self, *args, **kwargs):
        self.csf = ChannelSearchForm()


class ChannelsView(BaseChatView):
    decorators = [login_required]

    def dispatch_request(self):
        name = request.args.get('name')
        if name:
            channels = Channel.query.filter(
                Channel.name.like('%'+name+'%')
            ).all()
        else:
            channels = Channel.query.all()
        context = {"channels": channels, 'search_form': self.csf}
        return render_template('channels.html', **context)


class ChannelView(BaseChatView):
    decorators = [login_required]

    def dispatch_request(self, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        messages = Message.query.filter_by(channel_id=channel.id)
        context = dict(channel=channel, messages=messages, user=current_user)
        context.update(search_form=self.csf)
        return render_template('chat.html', **context)


class LoginView(View):
    methods = ['GET', 'POST']

    def get_user_data(self, form):
        user_data = form.data
        remember_me = user_data.pop('remember_me')
        return user_data, remember_me

    def dispatch_request(self):
        if current_user.is_authenticated():
            return redirect(url_for('channels'))

        signup_form = SignUpForm(prefix="signup")
        if signup_form.validate_on_submit():
            user_data, remember_me = self.get_user_data(signup_form)
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=remember_me)
            return redirect(url_for('channels'))

        signin_form = SignInForm(prefix="signin")
        if signin_form.validate_on_submit():
            user_data, remember_me = self.get_user_data(signin_form)
            user = User.query.filter_by(**user_data).first()
            if not user:
                return redirect(url_for('login'))
            login_user(user, remember_me)
            return redirect(url_for('channels'))

        return render_template(
            'login.html',
            signin_form=signin_form,
            signup_form=signup_form
            )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/channel/search', methods=['POST'])
@login_required
def channel_search():
    csf = ChannelSearchForm()
    if csf.validate_on_submit():
        name = csf.data.get('name')
    else:
        name = ''
    return redirect(url_for('channels', name=name))


@app.route('/channel/create', methods=['POST'])
@login_required
def create():
    name = request.form.get("name")
    if name:
        channel, created = get_or_create(db.session, Channel, name=name)
        return redirect(url_for('channel', channel_id=channel.id))
    return redirect(url_for('channels'))


@app.route('/socket.io/<path:path>')
def run_socketio(path):
    real_request = request._get_current_object()
    try:
        socketio_manage(
            request.environ,
            {'/chat': ChatNamespace},
            request=real_request
        )
    except ValueError:
        app.logger.error("Exception while handling socketio connecdtion",
                         exc_info=True)
    return Response()


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/', view_func=ChannelsView.as_view('channels'))
app.add_url_rule(
    '/channel/<int:channel_id>',
    view_func=ChannelView.as_view('channel')
)
