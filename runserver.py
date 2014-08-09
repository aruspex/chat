from chat import app

from gevent import monkey
from socketio.server import SocketIOServer


monkey.patch_all()


SocketIOServer(('', 5000), app, resource="socket.io").serve_forever()