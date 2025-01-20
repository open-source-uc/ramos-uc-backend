from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date
import re

class UserAccountCreate(BaseModel):
    email: EmailStr  
    password: str = Field(..., min_length=8) 
    nickname: str = Field(..., max_length=100)  
    admision_year: int  
    carrer_name: str

    @field_validator('admision_year')
    def validate_admision_year(cls, v):
        current_year = date.today().year
        if not (current_year - 12 <= v <= current_year):
            raise ValueError(f"El año de admisión debe estar entre {current_year - 12} y {current_year}.")
        return v
    
    @field_validator('password')
    def validate_password2(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe contener al menos un número.')
        return v
    
    @field_validator('email')
    def validate_password(cls, v: str):
        if not (v.endswith(".uc.cl") or v.endswith("@uc.cl")) :
            raise ValueError('Email no es de uc.cl')
        return v


