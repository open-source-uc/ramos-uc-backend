from pydantic import BaseModel, field_validator, EmailStr
import re

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str

class Rate(BaseModel):
    ramo_id: str
    rating: str

#User
class Login(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('email')
    def check_email_domain(cls, v):
        if not v.endswith('@uc.cl') or not v.endswith('@estudiante.uc.cl'):
            raise ValueError('Email Inválido. Tu email no es UC.')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        errores = []

        if len(v) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r"[A-Z]", v):
            errores.append('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r"[a-z]", v):
            errores.append('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r"[0-9]", v):
            errores.append('La contraseña debe contener al menos un número')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):  # Caracteres especiales
            errores.append('La contraseña debe contener al menos un carácter especial')
        if errores:
            raise ValueError(', '.join(errores)) 
        return v
