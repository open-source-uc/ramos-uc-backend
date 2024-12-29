import os
import jwt
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, Depends, Header
from fastapi.security import APIKeyHeader, APIKeyCookie
from bson import ObjectId
from pydantic import BaseModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", None)
assert SECRET_KEY is not None, "ERROR: SECRET_KEY no está configurada en las variables de entorno."

class Payload(BaseModel):
    user_id: str

def generar_token(user_id: str):
    payload = {
       "user_id": user_id
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

    
def decode_token(token):
    try:
        payload = jwt.decode(token.encode("utf-8"), SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token/Session Expired")
    except jwt.InvalidTokenError as error:
        raise HTTPException(401, detail="Invalid Token/Session")

    return payload


def proteger(
    session: str | None = Depends(APIKeyCookie(name="session", auto_error=False)),
) -> Payload:
    if session is None:
        raise HTTPException(401)

    try:
        payload: dict = decode_token(session)

        payload = Payload(
            user_id=payload.get("user_id"),
        )

    except HTTPException as error:
        raise error

    return payload