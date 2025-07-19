import os
import json
from utils.debug import log_func
import socketio

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def load_chat(data) -> None:
        id_chat = data.get("idChat")
        if not id_chat:
            log_func("Error: idChat not provided in data")
            return

        chat_dir = os.path.join("..", "data", "chats", id_chat)
        messages = []

        try:
            if not os.path.isdir(chat_dir):
                log_func(f"Error: Chat directory not found: {chat_dir}")
                return

            for filename in os.listdir(chat_dir):
                if filename == "config.json" or not filename.endswith(".json"):
                    continue

                filepath = os.path.join(chat_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = json.load(f)
                        messages.append(content)
                except Exception as e:
                    log_func(f"Error reading file {filepath}: {e}")

            senders = [int(m["sender"]) for m in messages if "sender" in m and m["sender"].isdigit()]

            sio.emit("get_info_users", {"users": senders, "type": "server", "server": {
                "chatId": id_chat,
                "messages": messages,
                "userId": data.get("from"),
                "type": "load_chat",
                "idUserServer": data.get("idUserServer")
            }})

        except Exception as e:
            log_func(f"Unexpected error loading chat {id_chat}: {e}")
