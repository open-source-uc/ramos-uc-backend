from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import accounts_collection
from database.schemas import Login
from bson import ObjectId
from lib.auth.encrypt import encriptar_password, validacion_password

router = APIRouter()

@router.post("/accounts")
async def create_usr(email: str, password: str):
    if accounts_collection.find_one({"email": email}):
        raise HTTPException("Usuario ya existente")
    hashed_password = encriptar_password(password)
    usuario = Login(email, hashed_password)
    accounts_collection.insert_one(usuario)
    return JSONResponse({"message": "Ok"})