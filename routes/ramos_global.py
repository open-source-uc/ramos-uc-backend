from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from database.database import ramos_collection
from database.schemas import Ramo, Rate
from bson import ObjectId

router = APIRouter()

@router.get("/", response_class=JSONResponse)
async def hello_world():
    return JSONResponse(content={"message": "Hello, World!"})


@router.get("/ramos_global", response_class=JSONResponse, response_model=Ramo)
async def get_ramos_global(
    id: Optional[str] = Query(None),
    sigle: Optional[str] = Query(None), 
    name: Optional[str] = Query(None), 
    credits: Optional[int] = Query(None), 
    school: Optional[str] = Query(None),  
    area: Optional[str] = Query(None), 
):
    query_filter = {}
    if id:
        query_filter["_id"] = id  
    if sigle:
        query_filter["sigle"] = sigle
    if name:
        query_filter["name"] = name
    if credits:
        query_filter["credits"] = credits
    if school:
        query_filter["school"] = school
    if area:
        query_filter["area"] = area

    result = list(ramos_collection.find(query_filter))
    result = list(map(lambda r: {"id": str(r["_id"]), **{k: v for k, v in r.items() if k != '_id'}}, result))
    return JSONResponse(content=result)

# @router.post("/ramos_global", response_class=JSONResponse)
# async def create_ramo(ramo: Ramo):
#     result = ramos_collection.insert_one(dict(ramo))
    
#     return JSONResponse(content={"id": str(result.inserted_id), **dict(ramo)}, status_code=201)

