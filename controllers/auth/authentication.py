from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models.authentication.authentication import TokenData

PWDCONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_member = OAuth2PasswordBearer(
    tokenUrl="guest/auth/login", scheme_name="member_oauth2_schema"
)


def create_token(user: dict):
    data = TokenData(
        userId=str(user["_id"]),
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    encoded_jwt = jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tokenData = TokenData(
            userId=payload.get("userId"),
            exp=payload.get("exp"),
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Token tidak valid")

    return tokenData
