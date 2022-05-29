import socketio

# standard Python
sio = socketio.Client()

sio.connect('https://socket-server-cc.herokuapp.com/')


@sio.event
def message(data):
    print('I received a message!')

