from utils.debug import log_func
from services.utils.transform import transform_avatar
import socketio
import os
import json

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def del_user_in_chat(data) -> None:
        chat_id = data.get("idChat")
        user_id = str(data.get("userId")).strip()

        if not chat_id or not user_id:
            log_func("Missing idChat or userId in the request")
            return

        config_path = os.path.join("..", "data", "chats", chat_id, "config.json")

        try:
            if not os.path.exists(config_path):
                log_func(f"Config file not found: {config_path}")
                return

            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            participants = config.get("participants", [])

            if user_id in participants:
                participants.remove(user_id)
                config["participants"] = participants

                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)

                log_func(f"User {user_id} removed from chat {chat_id}")
            else:
                log_func(f"[{chat_id}] User {user_id} not found in participants")

            sio.emit("updata_chat_server", {"dataChat": transform_avatar(config)})

        except Exception as e:
            log_func(f"Error updating config.json for chat {chat_id}: {e}")
