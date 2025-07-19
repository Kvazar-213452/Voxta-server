import socketio
from utils.debug import log_func
from services.socket_events import all_setup_events
from services.utils.code import generate_secure_token
from services.utils.utils import get_chats

sio = socketio.Client()
id_client: str

for setup in all_setup_events: setup(sio)

@sio.event
def connect():
    log_func("Connected to server")
    sio.emit("authenticate", {"token": "server", "chats": get_chats()})

@sio.event
def authenticated(data):
    if data.get("code") == 1:
        global id_client
        log_func(f"Authenticated on server id: {data.get("id")}")
        id_client = data.get("id")
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
