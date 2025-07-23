from utils.debug import log_func
from services.utils.transform import transform_avatar
from services.utils.upload_avatar import upload_avatar
import socketio
import os
import json

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def save_settings_chat(data) -> None:
        chat_id = data.get("idChat")
        new_data = data.get("dataChat", {})

        if not chat_id:
            log_func("idChat not provided")
            return

        config_path = os.path.join("..", "data", "chats", chat_id, "config.json")

        try:
            if not os.path.exists(config_path):
                log_func(f"Config file not found: {config_path}")
                return

            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            config["name"] = new_data.get("name", config.get("name"))
            config["desc"] = new_data.get("desc", config.get("desc"))
            if new_data.get("avatar") is not None:
                config["avatar"] = upload_avatar(new_data.get("avatar"))

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            sio.emit("updata_chat_server", {"dataChat": transform_avatar(config)})

        except Exception as e:
            log_func(f"Error updating chat config: {e}")
