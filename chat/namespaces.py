from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin

from flask.ext.login import current_user

from . import app, db
from .models import Message


class ChatNamespace(BaseNamespace, RoomsMixin):

    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        self.ctx = None
        if request:
            self.ctx = app.request_context(request.environ)
            self.ctx.push()
            app.preprocess_request()
            del kwargs['request']
        super(ChatNamespace, self).__init__(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        if self.ctx:
            self.ctx = None
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_join(self, channel):
        self.channel = str(channel)
        self.join(self.channel)

    def recv_disconnect(self):
        self.leave(self.channel)

    def on_new_message(self, text):
        msg = Message(
            text=text,
            user=current_user,
            channel_id=self.channel,
        )
        db.session.add(msg)
        db.session.commit()
        self.emit_to_room(
            self.channel,
            'msg_channel',
            current_user.name,
            text
        )
