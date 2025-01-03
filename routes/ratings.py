from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Cookie
from fastapi.responses import JSONResponse
from database.database import ramos_collection, accounts_collection
from database.schemas import Rate, Ramo
from fastapi.security import OAuth2PasswordBearer
from utils.auth.token import Payload, proteger
from utils.AI_Mod import moderar_comentario
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="ramosuc_token")


@router.post("/ratings/{ramo_id}")
async def create_rating(ramo_id: str, rating: Rate, payload: Payload = Depends(proteger)):

    ramo: Ramo = ramos_collection.find_one({"_id": ObjectId(ramo_id)})

    moderacion_bool = moderar_comentario(rating.comment)
    if moderacion_bool == False:
        pass

    if not ramo:
        raise HTTPException(status_code=404, detail="Ramo not found")
    
    ramo = Ramo(**ramo)
    rating.user_id = payload.user_id

    if rating.rating is True:
        ramo.positive_count = ramo.positive_count + 1
    else:
        ramo.negative_count = ramo.negative_count + 1

    # Agregar la nueva reseña al campo 'reviews'
    for review in ramo.reviews:
        if review.user_id == payload.user_id:
            raise HTTPException(status_code=409, detail="Ya comentaste en este curso")
    ramo.reviews.append(rating)
    # Guardar los cambios en la base de datos
    ramos_collection.update_one(
        {"_id": ObjectId(ramo_id)},
        {"$set": {"reviews": list(map(lambda review: review.model_dump(), ramo.reviews)), "positive_count": ramo.positive_count, "negative_count": ramo.negative_count }}
    )

    
    return JSONResponse(content={"message": "ok"}, status_code=200)

@router.get("/ratings/{ramo_id}", response_model=List[Rate])
async def get_ramo_ratings(ramo_id: str): #Agregar un sistema de paginacion maybe
    ramo: Ramo = ramos_collection.find_one({"_id": ObjectId(ramo_id)})
    result = list([ramo])
    result = list(map(lambda r: {"id": str(r["_id"]), **{k: v for k, v in r.items() if k != '_id'}}, result))
    return JSONResponse(content=result)
