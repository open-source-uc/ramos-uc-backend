from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
import sqlalchemy
from database.database import get_db, Course, Review
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from utils.auth.token import proteger_user, Payload
from utils.validators.reviews import ReviewCreate

router = APIRouter()

@router.get("/reviews/{sigle}")
async def get_reviews(   
    sigle: str, 
    page: int = Query(0),
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter_by(section_sigle=sigle, status='visible').offset(page * 100).limit(100).all()
    return reviews

@router.post("/reviews")
async def create_review(   
    body: ReviewCreate,
    payload: Payload = Depends(proteger_user),
    db: Session = Depends(get_db)
):
    existing_review = db.query(Review).filter_by(section_sigle = body.section_sigle, email_hash=payload.user_id).first()
    if existing_review:
        return JSONResponse(
            {"msg": "Review already exists"},
            status_code=409, 
        )
    
    new_review = Review(
        section_sigle = body.section_sigle,
        section_number = body.section_number,
        year = body.year,
        semester = body.semester,
        email_hash = payload.user_id,
        liked = body.liked,
        comment = body.comment,
        estimated_credits = body.estimated_credits,
        status = "visible"
    )

    try:
        db.add(new_review)
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        return JSONResponse({
            "msg": "Integrity error occurred",
        }, status_code=409)
    finally:
        db.close()

    return JSONResponse({"msg": "ok"})

@router.put("/reviews")
async def update_review(
    body: ReviewCreate,
    payload: Payload = Depends(proteger_user),
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter_by(section_sigle = body.section_sigle, email_hash=payload.user_id).first()
    
    if not review:
        return JSONResponse(
            {"msg": "Review not found or not authorized to update"},
            status_code=404,
        )
    
    review.section_sigle = body.section_sigle
    review.section_number = body.section_number
    review.year = body.year
    review.semester = body.semester
    review.liked = body.liked
    review.comment = body.comment
    review.estimated_credits = body.estimated_credits
    review.status = "visible"

    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        return JSONResponse({
            "msg": "Integrity error occurred",
        }, status_code=409)
    finally:
        db.close()

    return JSONResponse({"msg": "Review updated"})

@router.delete("/reviews/{sigle}")
async def delete_review(
    sigle: str,
    payload: Payload = Depends(proteger_user),
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter_by(section_sigle = sigle, email_hash=payload.user_id).first()
    
    if not review:
        return JSONResponse(
            {"msg": "Review not found or not authorized to delete"},
            status_code=404,
        )
    
    try:
        db.delete(review)
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        return JSONResponse({
            "msg": "Integrity error occurred",
        }, status_code=409)
    finally:
        db.close()

    return JSONResponse({"msg": "Review deleted"})
