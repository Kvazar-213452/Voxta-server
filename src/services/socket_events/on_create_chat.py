from utils.debug import log_func
from utils.code import generate_secure_token
import socketio

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def create_chat(data) -> None:
        log_func(f"Received create_chat event: {data}")

        generate_secure_token()
