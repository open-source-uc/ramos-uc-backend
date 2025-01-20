from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
import sqlalchemy
from database.database import get_db, UserAccount
from utils.auth.encrypt import encriptar_password, validacion_password, hash_text
from utils.auth.token import generar_token
from sqlalchemy.orm import Session
from utils.validators.auth import UserAccountCreate
router = APIRouter()

@router.post("/accounts/register")
async def create_user(account: UserAccountCreate, db: Session = Depends(get_db)):
    email_hash = hash_text(account.email)
    existing_user = db.query(UserAccount).filter_by(email_hash=email_hash).first()
    if existing_user:
        return JSONResponse(
            {"msg": "A user with this email already exists"},
            status_code=409, 
        )
    
    new_user = UserAccount(
        email_hash=email_hash,
        password=encriptar_password(account.password),
        nickname=account.nickname,
        admision_year=account.admision_year,
        carrer_name=account.carrer_name,
    )
    try:
        db.add(new_user)
        db.commit()
        token = generar_token(email_hash)
    except sqlalchemy.exc.IntegrityError as error:
        return JSONResponse({
            "msg": "Integrity error occurred",
        }, status_code=409)
    finally:
        db.close()

    return JSONResponse({"msg": "ok", "token": token, "name": account.nickname})


@router.post("/accounts/login")
async def login_user(
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    email_hash = hash_text(email)

    user = db.query(UserAccount).filter_by(email_hash=email_hash).first()
    if not user:
        return JSONResponse(
            {"msg": "Invalid email or password"},
            status_code=401
        )

    if not validacion_password(password, user.password):
        return JSONResponse(
            {"msg": "Invalid email or password"},
            status_code=401
        )

    token = generar_token(email_hash)

    return JSONResponse({"msg": "ok", "token": token, "name": user.nickname})