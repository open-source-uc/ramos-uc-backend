from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from database.database import accounts_collection
from database.schemas import User
from utils.auth.encrypt import encriptar_password, validacion_password
from utils.auth.token import generar_token
import re

router = APIRouter()

@router.post("/accounts/register")
async def create_usr(account: User):
    if accounts_collection.find_one({"email": account.email}) is not None:
        raise HTTPException(detail="Usuario ya existente", status_code=409)
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
        raise HTTPException(detail=', '.join(errores), status_code=400)
    #No hay molleha (monejo code)

    hashed_password = encriptar_password(account.password)
    account.password = hashed_password
    result = accounts_collection.insert_one(account.model_dump())

    token = generar_token(str(result.inserted_id))
    return JSONResponse({"message": "Ok", "token": token, "name": account.name})

@router.post("/accounts/login")
async def login_usr(email: str = Body(...), password: str = Body(...)):
    account = accounts_collection.find_one({"email": email})
    if not account:
        raise HTTPException(detail="Usuario no existe", status_code=404)
    user_id = account["_id"]
    account = User(**account)
    if not validacion_password(password, account.password):
        raise HTTPException(detail="La contraseña no es correcta", status_code=401)
    token = generar_token(str(user_id))
    return JSONResponse({"message": "Ok", "token": token, "name": account.name})