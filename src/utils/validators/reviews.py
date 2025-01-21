from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date
import re

class ReviewCreate(BaseModel):
    section_sigle: str = Field(..., max_length=50)
    section_number: int
    year: int
    semester: int
    liked: bool
    comment: str = Field(..., max_length=500)
    estimated_credits: int = Field(..., ge=0, le=30)
    

