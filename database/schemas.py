from pydantic import BaseModel, Field, field_validator
from typing import List
from enum import Enum

class Rate(BaseModel):
    rating: bool  # Booleano para que sea como bueno o malo (True = bueno, False = malo)
    comment: str  # Comentario de la reseña
    profesor: str
    year: int
    semestre: int | str
    user_id: str  # ID del usuario que dejó la reseña
    creditos_presuntos: int # Los creditos que pensas que valen x ejemplo BBDD vale 10 pero es como 30

    @field_validator('semestre')
    def validate_semestre(cls, value):
        if value in ["TAV", 1, 2]:
            return value
        else:
            raise ValueError(f"El valor numérico {value} no corresponde a un semestre válido.")
       

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str
    reviews: List[Rate] = Field(default_factory=list)  # Lista de reseñas asociadas al ramo
    positive_count: int = 0
    negative_count: int = 0