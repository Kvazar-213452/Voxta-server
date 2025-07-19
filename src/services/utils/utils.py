import os
import json
from services.utils.transform import transform_avatar

def get_chats() -> list[dict]:
    chat_dir = os.path.join("..", "data", "chats")
    if not os.path.exists(chat_dir):
        return []

    chats = []

    for name in os.listdir(chat_dir):
        dir_path = os.path.join(chat_dir, name)
        config_path = os.path.join(dir_path, "config.json")

        if os.path.isdir(dir_path) and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    chats.append(transform_avatar(config_data))
            except Exception as e:
                print(f"Помилка при читанні {config_path}: {e}")

    return chats
