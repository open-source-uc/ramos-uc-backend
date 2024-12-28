from pydantic import BaseModel, Field
from typing import List

class Rate(BaseModel):
    rating: bool  # Booleano para que sea como bueno o malo (True = bueno, False = malo)
    comment: str  # Comentario de la reseña
    user_id: str  # ID del usuario que dejó la reseña

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str
    reviews: List[Rate] = Field(default_factory=list)  # Lista de reseñas asociadas al ramo
    positive_count: int = 0
    negative_count: int = 0