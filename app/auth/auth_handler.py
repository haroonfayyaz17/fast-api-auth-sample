import os
from dotenv import load_dotenv
import time
from typing import Dict
import jwt

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: dict) -> Dict[str, str]:
    payload = {
        **user,
        "expires": time.time() + 7 * 24 * 3600  # 7 days
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
