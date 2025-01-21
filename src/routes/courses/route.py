from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from database.database import get_db, Course, Review
from sqlalchemy.orm import Session
from sqlalchemy import func, case

router = APIRouter()

@router.get("/")
async def get_courses(
    page: int = Query(0),
    sigle: str = Query(None, description="Sigla del curso a filtrar"),
    area: str = Query(None, description="Área del curso a filtrar"),
    db: Session = Depends(get_db)
):
    query = db.query(
        Course.sigle,
        func.coalesce(
            func.avg(
                case(
                    (Review.liked == True, 1),
                    else_=0
                )
            ),
            None
        ).label("average_liked"),
        func.coalesce(func.avg(Review.estimated_credits), None).label("average_estimated_credits")
    ).join(Review, Course.sigle == Review.section_sigle, isouter=True)
    
    if sigle:
        query = query.filter_by(Course.sigle == sigle)
    
    if area:
        query = query.filter_by(Course.area == area)
    
    query = query.group_by(Course.sigle).order_by(func.coalesce(func.avg(
        case(
            (Review.liked == True, 1),
            else_=0
        )
    ), 0).desc())

    courses = query.offset(page * 100).limit(100).all()
    
    return {
        "msg": "ok",
        "courses": [{"course": course, "average_liked": avg_liked if avg_liked != 0 else None, "average_estimated_credits": avg_credits} for course, avg_liked, avg_credits in courses]
    }

