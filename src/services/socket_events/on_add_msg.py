from utils.debug import log_func
import socketio

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def add_msg(data) -> None:
        log_func(f"Received create_chat event: {data}")
