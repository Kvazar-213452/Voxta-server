from .on_create_chat import setup_events as setup_events_create_chat
from .on_send_msg import setup_events as setup_events_add_msg
from .on_load_chat import setup_events as setup_events_load_chat
from .on_get_lite_key import setup_events as setup_get_lite_key
from .on_save_settings_chat import setup_events as setup_get_save_settings_chat
from .on_del_user_in_chat import setup_events as setup_get_del_user_in_chat
from .on_add_user_in_chat import setup_events as setup_get_add_user_in_chat

all_setup_events = [
    setup_events_create_chat,
    setup_events_add_msg,
    setup_events_load_chat,
    setup_get_lite_key,
    setup_get_save_settings_chat,
    setup_get_del_user_in_chat,
    setup_get_add_user_in_chat,
]
