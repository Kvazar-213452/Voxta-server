import os
import base64
import uuid

def upload_avatar(base64_avatar: str) -> str:
    avatar_dir = os.path.join("..", "data", "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    
    avatar_id = str(uuid.uuid4())
    file_name = f"{avatar_id}.png"
    file_path = os.path.join(avatar_dir, file_name)

    if base64_avatar.startswith("data:image"):
        base64_avatar = base64_avatar.split(",")[1]

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64_avatar))

    return f"../data/avatars/{file_name}"
