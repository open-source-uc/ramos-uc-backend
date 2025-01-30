import os
from typing import List
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.database import get_db, UserPermission

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


def proteger_admin(
    token: str | None = Depends(APIKeyHeader(name="token", auto_error=False)),
    db: Session = Depends(get_db),
) -> Payload:
    if token is None:
        raise HTTPException(401)

    try:
        payload = decode_token(token)

        payload = Payload(
            user_id=payload["user_id"],
        )

    except HTTPException as error:
        raise error
    
    permissions = db.query(UserPermission).filter(UserPermission.email_hash == payload.user_id).all()
    permissions = [i.permission_name for i in permissions]

    required_permissions = ["SUDO"]

    for i in required_permissions:
        if i not in permissions:
            raise HTTPException(403, detail="Permission Denied")

    return payload

def proteger_user(
    token: str | None = Depends(APIKeyHeader(name="token", auto_error=False)),
    db: Session = Depends(get_db),
) -> Payload:
    if token is None:
        raise HTTPException(401)

    try:
        payload = decode_token(token)

        payload = Payload(
            user_id=payload["user_id"],
        )

    except HTTPException as error:
        raise error
    
    permissions = db.query(UserPermission).filter(UserPermission.email_hash == payload.user_id).all()
    permissions = [i.permission_name for i in permissions]

    required_permissions = ["CREATE_EDIT_OWN_REVIEW"]

    for i in required_permissions:
        if i not in permissions:
            raise HTTPException(403, detail="Permission Denied")

    return payload


def proteger_only_token(
    token: str | None = Depends(APIKeyHeader(name="token", auto_error=False)),
) -> Payload:
    if token is None:
        raise HTTPException(401)

    try:
        payload = decode_token(token)

        payload = Payload(
            user_id=payload["user_id"],
        )

    except HTTPException as error:
        raise error

    return payload