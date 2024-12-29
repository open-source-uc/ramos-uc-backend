from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import accounts_collection
from database.schemas import User
from utils.auth.encrypt import encriptar_password, validacion_password
import re

router = APIRouter()

@router.post("/accounts/register")
async def create_usr(account: User):
    if accounts_collection.find_one({"email": account.email}) is not None:
        raise HTTPException("Usuario ya existente", status_code=409)
    #No hay molleha (monejo code)
    errores = []
    if len(account.password) < 8:
        errores.append('La contraseña debe tener al menos 8 caracteres')
    if not re.search(r"[A-Z]", account.password):
        errores.append('La contraseña debe contener al menos una letra mayúscula')
    if not re.search(r"[a-z]", account.password):
        errores.append('La contraseña debe contener al menos una letra minúscula')
    if not re.search(r"[0-9]", account.password):
        errores.append('La contraseña debe contener al menos un número')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", account.password):  # Caracteres especiales
        errores.append('La contraseña debe contener al menos un carácter especial')
    if errores:
        raise HTTPException(', '.join(errores), status_code=400)
    #No hay molleha (monejo code)
    hashed_password = encriptar_password(account.password)
    account.password = hashed_password
    accounts_collection.insert_one(account)
    return JSONResponse({"message": "Ok"})

@router.post("/accounts/login")
async def login_usr(email: str, password: str):
    account = accounts_collection.find_one({"email": email})
    if not account:
        raise HTTPException("Usuario no existe", status_code=404)
    account = User(**account)
    if not validacion_password(password, account.password):
        raise HTTPException("La contraseña no es correcta", status_code=401)
    return JSONResponse({"message": "Ok"})