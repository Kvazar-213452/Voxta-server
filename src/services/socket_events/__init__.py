from .on_create_chat import setup_events as setup_events_create_chat
from .on_add_msg import setup_events as setup_events_add_msg

all_setup_events = [
    setup_events_create_chat,
    setup_events_add_msg,
]
