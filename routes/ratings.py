from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import ramos_collection, ratings_collection
from database.schemas import Rate
from bson import ObjectId

router = APIRouter()

@router.post("/ratings", response_model=Rate)
async def create_rating(rating: Rate): #Hay que añadir para verificar si un usuario ya hizo el rating
    ramo = ramos_collection.find_one({"_id": ObjectId(rating.ramo_id)})
    if not ramo:
        raise HTTPException(status_code=404, detail="Ramo not found")
    
    rating_dict = rating.dict()
    result = ratings_collection.insert_one(rating_dict)
    
    return {
        "id": str(result.inserted_id),
        **rating_dict
    }

@router.get("/ratings/{ramo_id}", response_model=List[Rate])
async def get_ramo_ratings(ramo_id: str): #Agregar un sistema de paginacion maybe
    ratings = list(ratings_collection.find({"ramo_id": ramo_id}))
    return [
        {
            "id": str(rating["_id"]),
            **{k: v for k, v in rating.items() if k != "_id"}
        }
        for rating in ratings
    ]

# Agregar endpoint para estadísticas
@router.get("/ratings/stats/{ramo_id}")
async def get_rating_stats(ramo_id: str):
    ratings = list(ratings_collection.find({"ramo_id": ramo_id}))
    
    positive_count = sum(1 for r in ratings if r["rating"])
    total_ratings = len(ratings)
    
    return {
        "positive_count": positive_count,
        "negative_count": total_ratings - positive_count,
        "total_ratings": total_ratings
    }