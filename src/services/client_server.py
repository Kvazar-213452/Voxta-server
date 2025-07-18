import socketio
from utils.debug import log_func
from services.socket_events import all_setup_events
from utils.code import generate_secure_token

sio = socketio.Client()

for setup in all_setup_events: setup(sio)

@sio.event
def connect():
    log_func("Connected to server")
    sio.emit("authenticate", {"token": "server"})

@sio.event
def authenticated(data):
    if data.get("code") == 1:
        log_func("Authenticated on server")
        generate_secure_token()

@sio.event
def connect_error(data):
    log_func("Connection failed:", data)

@sio.event
def disconnect():
    log_func("Disconnected from server")

def connect_to_socket_server():
    try:
        sio.connect('http://localhost:3001')
        sio.wait()
    except Exception as e:
        log_func("Exception occurred during connect:", e)
