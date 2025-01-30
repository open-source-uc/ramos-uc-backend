from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
import sqlalchemy
from database.database import Review, get_db, UserAccount, UserPermission
from sqlalchemy.orm import Session

from utils.auth.encrypt import encriptar_password
from utils.auth.token import Payload, proteger_user, proteger_only_token
from utils.validators.auth import UserAccountModify
import re

router = APIRouter()

@router.get("/")
async def get_reviews(db: Session = Depends(get_db), payload: Payload = Depends(proteger_only_token)):
    result = db.query(UserAccount).outerjoin(UserPermission, UserAccount.email_hash == UserPermission.email_hash).filter(UserAccount.email_hash == payload.user_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    permissions = db.query(UserPermission).filter(UserPermission.email_hash == payload.user_id).all()

    return JSONResponse(content={
        "user": {
            "admision_year": result.admision_year,
            "carrer_name": result.carrer_name,
            "nickname": result.nickname,
        },
        "permissions": [i.permission_name for i in permissions] if permissions else []
    }, status_code=200)

@router.put("/")
async def update_user(
    update_data: UserAccountModify,
    db: Session = Depends(get_db),
    payload: Payload = Depends(proteger_only_token),
):
    user = db.query(UserAccount).filter(UserAccount.email_hash == payload.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.admision_year = update_data.admision_year
    user.carrer_name = update_data.carrer_name
    user.nickname = update_data.nickname

    db.commit()

    return JSONResponse(content={
        "user": {
            "admision_year": user.admision_year,
            "carrer_name": user.carrer_name,
            "nickname": user.nickname,
        }
    }, status_code=200)

@router.patch("/")
async def update_user_password(
    new_password: str = Body(...),
    db: Session = Depends(get_db),
    payload: Payload = Depends(proteger_only_token),
):
    user = db.query(UserAccount).filter(UserAccount.email_hash == payload.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if len(new_password) < 8:
        raise HTTPException('La contraseña debe tener al menos 8 caracteres.')
    if not re.search(r'[A-Z]', new_password):
        raise HTTPException('La contraseña debe contener al menos una letra mayúscula.')
    if not re.search(r'[0-9]', new_password):
        raise HTTPException('La contraseña debe contener al menos un número.')
    
    user.password = encriptar_password(new_password)

    db.commit()

    return JSONResponse(content={
        "msg": "Password updated"
    }, status_code=200)

@router.delete("/")
async def delete_user(
    db: Session = Depends(get_db),
    payload: Payload = Depends(proteger_only_token),
):
    user = db.query(UserAccount).filter(UserAccount.email_hash == payload.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Review).filter(Review.email_hash == user.email_hash).delete()

    db.delete(user)
    db.commit()

    return JSONResponse(content={
        "msg": "User deleted successfully"
    }, status_code=200)
