import time
from typing import Dict
import jwt

from config.config import Settings

secret_key = Settings().secret_key


def sign_jwt(user_id: str) -> str:
    # Set the expiry time.
    payload = {"user_id": user_id, "expires": time.time() + 2400}
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token
