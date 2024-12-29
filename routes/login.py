from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import accounts_collection
from database.schemas import Login
from bson import ObjectId
from lib.auth.encrypt import encriptar_password, validacion_password

router = APIRouter()

@router.post("/accounts/register")
async def create_usr(email: str, password: str):
    if accounts_collection.find_one({"email": email}) is not None:
        raise HTTPException("Usuario ya existente", status_code=409)
    hashed_password = encriptar_password(password)
    usuario = Login(email, hashed_password)
    accounts_collection.insert_one(usuario)
    return JSONResponse({"message": "Ok"})

@router.post("/accounts/login")
async def login_usr(email: str, password: str):
    account = accounts_collection.find_one({"email": email})
    if not account:
        raise HTTPException("Usuario no existe", status_code=404)
    account = Login(**account)
    if not validacion_password(password, account.password):
        raise HTTPException("La contraseña no es correcta", status_code=401)
    return JSONResponse({"message": "Ok"})