from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from database.database import get_db, Course, Review
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from enum import Enum

router = APIRouter()

class AreaEnum(str, Enum):
    ciencias_sociales = "Ciencias Sociales"
    humanidades = "Humanidades"
    pensamiento_matematico = "Pensamiento Matemático"
    salud_bienestar = "Salud y Bienestar"
    artes = "Artes"
    formacion_teologica = "Formación Teológica"
    ecologia_sustentabilidad = "Ecología Integral y Sustentabilidad"
    formacion_filosofica = "Formación Filosófica"
    ciencia_tecnologia = "Ciencia y Tecnología"


@router.get("/")
async def get_courses(
    page: int = Query(0),
    sigle: str = Query(None, description="Sigla del curso a filtrar"),
    area: AreaEnum = Query(None, description="Área del curso a filtrar"),
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            Course.sigle,
            Course.area,
            func.coalesce(
                func.avg(
                    case(
                        (Review.liked == True, 1),
                        else_=0
                    )
                ),
                0
            ).label("average_liked"),
            func.coalesce(func.avg(Review.estimated_credits), 0).label("average_estimated_credits")
        )
        .join(Review, Course.sigle == Review.section_sigle, isouter=True)
    )

    if sigle:
        query = query.filter(func.upper(Course.sigle).startswith(sigle.upper()))

    if area:
        query = query.filter(func.upper(Course.area).startswith(area.upper()))

    query = (
        query.group_by(Course.sigle, Course.area)
        .order_by(
            func.coalesce(
                func.avg(
                    case(
                        (Review.liked == True, 1),
                        else_=0
                    )
                ),
                0
            ).desc()
        )
    )

    # Paginación
    courses = query.offset(page * 100).limit(100).all()

    
    return {
        "msg": "ok",
        "courses": [{
            "course": course, 
            "average_liked": avg_liked if avg_liked != 0 else None, 
            "average_estimated_credits": avg_credits if avg_credits != 0 else None,
            "area": area} 
            for course, area, avg_liked, avg_credits in courses
        ]
    }

