from utils.debug import log_func
from utils.crypto_utils.SPX_CriptoLite import get_key_lite, fast_decrypt
import socketio
import os
import json
import uuid

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def send_msg(data) -> None:
        log_func(f"Received send_msg event: {data}")

        decrypted_raw = fast_decrypt(data["message"], get_key_lite()["privateKey"])
        try:
            decrypted_message = json.loads(decrypted_raw)
        except json.JSONDecodeError:
            log_func("Помилка декодування JSON після дешифрування")
            return

        while True:
            msg_id = uuid.uuid4().hex
            id_chat = data.get("idChat")
            chat_dir = os.path.join("..", "data", "chats", id_chat)
            file_path = os.path.join(chat_dir, f"{msg_id}.json")
            if not os.path.exists(file_path):
                break

        os.makedirs(chat_dir, exist_ok=True)

        decrypted_message["_id"] = msg_id

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(decrypted_message, f, indent=2, ensure_ascii=False)

        log_func(f"Message saved to {file_path}")
