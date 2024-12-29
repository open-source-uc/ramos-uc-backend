from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import ramos_collection
from database.schemas import Rate, Ramo
from bson import ObjectId

router = APIRouter()

@router.post("/ratings/{ramo_id}")
async def create_rating(ramo_id: str, rating: Rate): #Hay que añadir para verificar si un usuario ya hizo el rating
    ramo: Ramo = ramos_collection.find_one({"_id": ObjectId(ramo_id)})
    if not ramo:
        raise HTTPException(status_code=404, detail="Ramo not found")
    
    rating_dict = dict(rating)

    # Asegurarse de que 'reviews' existe y es una lista, si no es así, inicializarla
    if 'reviews' not in ramo:
        ramo['reviews'] = []

    if rating.rating is True:
        ramo["positive_count"] = ramo.get("positive_count", 0) + 1
    else:
        ramo["negative_count"] = ramo.get("negative_count", 0) + 1

    # Agregar la nueva reseña al campo 'reviews'
    ramo['reviews'].append(rating_dict)

    # Guardar los cambios en la base de datos
    ramos_collection.update_one(
        {"_id": ObjectId(ramo_id)},
        {"$set": {"reviews": ramo['reviews'], "positive_count": ramo.get("positive_count", 0), "negative_count": ramo.get("negative_count", 0) }}
    )

    
    return {
        "id": str(ramo["_id"]), 
        "reviews": ramo['reviews']
    }

@router.get("/ratings/{ramo_id}", response_model=List[Rate])
async def get_ramo_ratings(ramo_id: str): #Agregar un sistema de paginacion maybe
    ramo: Ramo = ramos_collection.find_one({"_id": ObjectId(ramo_id)})
    ratings = ramo.get("reviews", [])
    return [
        {
            "ramo_id": str(ramo["_id"]),
            **{k: v for k, v in rating.items() if k != "_id"}
        }
        for rating in ratings
    ]