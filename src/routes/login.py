from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from database.database import get_db
from database.checks import User
from utils.auth.encrypt import encriptar_password, validacion_password
from utils.auth.token import generar_token
from sqlalchemy.orm import Session
import re
from database import tables
router = APIRouter()

@router.post("/accounts/register")
async def create_user(account: User, db: Session = Depends(get_db)):

    errores = []
    if len(account.contrasena) < 8:
        errores.append('La contraseña debe tener al menos 8 caracteres')
    if not re.search(r"[A-Z]", account.contrasena):
        errores.append('La contraseña debe contener al menos una letra mayúscula')
    if not re.search(r"[a-z]", account.contrasena):
        errores.append('La contraseña debe contener al menos una letra minúscula')
    if not re.search(r"[0-9]", account.contrasena):
        errores.append('La contraseña debe contener al menos un número')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", account.contrasena):
        errores.append('La contraseña debe contener al menos un carácter especial')
    if errores:
        raise HTTPException(detail=', '.join(errores), status_code=400)

    new_user = tables.Usuario(**account.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generar_token(new_user.correo)
    return JSONResponse({"message": "Ok", "token": token, "name": account.nombre})

# @router.post("/accounts/login")
# async def login_user(db: Session = Depends(get_db),email: str = Body(...), password: str = Body(...)):
#     account = accounts_collection.find_one({"email": email})
#     if not account:
#         raise HTTPException(detail="Usuario no existe", status_code=404)
#     user_id = account["_id"]
#     account = User(**account)
#     if not validacion_password(password, account.password):
#         raise HTTPException(detail="La contraseña no es correcta", status_code=401)
#     token = generar_token(str(user_id))
#     return JSONResponse({"message": "Ok", "token": token, "name": account.name})