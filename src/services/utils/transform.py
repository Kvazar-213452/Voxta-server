import base64
import os

def transform_avatar(chat: dict) -> dict:
    avatar_path = chat.get("avatar")

    if avatar_path and os.path.exists(avatar_path):
        with open(avatar_path, "rb") as f:
            image_data = f.read()
            base64_avatar = base64.b64encode(image_data).decode("utf-8")
            mime_type = "image/png"
            chat["avatar"] = f"data:{mime_type};base64,{base64_avatar}"
    else:
        chat["avatar"] = None

    return chat
