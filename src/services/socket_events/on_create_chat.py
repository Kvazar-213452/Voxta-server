import os
import json
import socketio
from datetime import datetime
from services.utils.code import generate_secure_token
from services.utils.upload_avatar import upload_avatar
from services.utils.transform import transform_avatar
from utils.debug import log_func

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def create_chat(data) -> None:
        chat_data = data.get("chat", {})
        chat_id = generate_secure_token(24)

        chat_dir = os.path.join("..", "data", "chats", chat_id)
        os.makedirs(chat_dir, exist_ok=True)

        config = {
            "id": chat_id,
            "type": "server",
            "avatar": upload_avatar(chat_data.get("avatar")),
            "participants": [data.get("from")],
            "name": chat_data.get("name", "Unnamed Chat"),
            "createdAt": chat_data.get("createdAt", datetime.utcnow().isoformat() + "Z"),
            "desc": chat_data.get("description", ""),
            "owner": data.get("from")
        }

        config_path = os.path.join(chat_dir, "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        log_func(f"Chat created at: {config_path}")

        sio.emit("send_new_chat_server", {"chat": transform_avatar(config)})
