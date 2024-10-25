from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database.database import ramos_collection, ratings_collection
from database.schemas import Ramo, Rate, User
from bson import ObjectId

router = APIRouter()

@router.post("/ramos", response_class=JSONResponse)
async def create_ramo(ramo: Ramo):
    result = ramos_collection.insert_one(ramo.dict())
    return JSONResponse(content={"id": str(result.inserted_id), **ramo.dict()}, status_code=201)

@router.get("/ramos", response_class=JSONResponse)
async def get_ramos():
    ramos = list(ramos_collection.find({}, {"_id": {"$toString": "$_id"}}))
    return JSONResponse(content=ramos)

@router.put("/ramos/{ramo_id}", response_class=JSONResponse)
async def update_ramo(ramo_id: str, ramo: Ramo):
    result = ramos_collection.update_one({"_id": ObjectId(ramo_id)}, {"$set": ramo.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="ramo not found")
    return JSONResponse(content={"message": "Ramo updated successfully"})

@router.delete("/ramos/{ramo_id}", response_class=JSONResponse)
async def delete_ramo(ramo_id: str):
    result = ramos_collection.delete_one({"_id": ObjectId(ramo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ramo not found")
    return JSONResponse(content={"message": "Ramo deleted successfully"})

@router.post("/rates", response_class=JSONResponse)
async def create_rate(rate: Rate):
    ramo = ramos_collection.find_one({"_id": ObjectId(rate.ramo_id)})
    if not ramo:
        raise HTTPException(status_code=404, detail="ramo not found")

    if rate.rating not in ["bueno", "regular", "malo"]:
        raise HTTPException(status_code=400, detail="Invalid rating")

    result = ratings_collection.insert_one(rate.dict())
    return JSONResponse(content={"id": str(result.inserted_id), **rate.dict()}, status_code=201)

@router.get("/ramos/{ramo_id}/rates", response_class=JSONResponse)
async def get_ramo_rates(ramo_id: str):
    ramo = ramos_collection.find_one({"_id": ObjectId(ramo_id)})
    if not ramo:
        raise HTTPException(status_code=404, detail="ramo not found")

    rates = list(ratings_collection.find({"ramo_id": ramo_id}, {"_id": 0}))
    good_rates = sum(1 for rate in rates if rate["rating"] == "bueno")
    regular_rates = sum(1 for rate in rates if rate["rating"] == "regular")
    bad_rates = sum(1 for rate in rates if rate["rating"] == "malo")

    return JSONResponse(content={
        "ramo_id": ramo_id,
        "total_rates": len(rates),
        "good_rates": good_rates,
        "regular_rates": regular_rates,
        "bad_rates": bad_rates
    })

@router.post("/register/")
async def create_user(user: User):
    pass
