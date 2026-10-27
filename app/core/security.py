from typing import Optional
import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import config
from app.core.scopes import ROLE_SCOPES_MAP

passwprd_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return passwprd_hash.hash(password)


def verify_hashed_password(hashed_password: str, password: str) -> bool:
    return passwprd_hash.verify(password, hashed_password)


def create_access_token(data: dict, expiration_minute: Optional[int] = None):
    encode_data = data.copy()

    if expiration_minute:
        expire_on = datetime.now(timezone.utc) + timedelta(minutes=expiration_minute)
    else:
        expire_on = datetime.now(timezone.utc) + timedelta(
            minutes=config.jwt_expiration_minute
        )

    encode_data.update({"exp": expire_on})

    scopes = ROLE_SCOPES_MAP[encode_data.get("role", "student")]

    encode_data.update({"scopes": scopes})

    return jwt.encode(
        payload=encode_data, key=config.jwt_secret_key, algorithm=config.jwt_algorithm
    )


def decode_access_token(token):
    return jwt.decode(
        jwt=token, key=config.jwt_secret_key, algorithms=[config.jwt_algorithm]
    )
