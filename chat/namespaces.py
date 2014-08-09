from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from flask.ext.login import current_user

from . import app, db
from .models import Message


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

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
            self.ctx.pop()
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_join(self, channel):
        self.channel = str(channel)
        self.join(self.channel)

    # def on_nickname(self, nickname):
    #     self.nicknames.append(nickname)
    #     self.session['nickname'] = nickname
    #     self.broadcast_event('announcement',
    #                          '{} has connected'.format(nickname))
    #     self.broadcast_event('nicknames', self.nicknames)
    #     return True, nickname

    # def recv_disconnect(self):
    #     nickname = self.session['nickname']
    #     self.nicknames.remove(nickname)
    #     self.broadcast_event('announcement',
    #                          '{} has disconnected'.format(nickname))
    #     self.broadcast_event('nicknames', self.nicknames)
    #     self.disconnect(silent=True)
    #     return True

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
