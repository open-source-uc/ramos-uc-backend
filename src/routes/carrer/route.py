from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from database.database import get_db, Career
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from enum import Enum
from sqlalchemy import and_

router = APIRouter()

@router.get("/")
async def get_courses(
    db: Session = Depends(get_db)
):

    query = db.query(Career).all()

    
    return {
        "msg": "ok",
        "carrers": query
    }
