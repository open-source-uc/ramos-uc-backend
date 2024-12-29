from pydantic import BaseModel, field_validator, EmailStr, Field
from typing import List
from typing import Any

carreras = [
  "Actuación",
  "Administración Pública",
  "Agronomía e Ingeniería Forestal",
  "Antropología – Arqueología",
  "Arquitectura",
  "Arte",
  "Astronomía",
  "Biología",
  "Biología Marina",
  "Bioquímica",
  "Ciencia Política",
  "College Artes y Humanidades",
  "College Ciencias Naturales y Matemáticas",
  "College Ciencias Sociales",
  "Construcción Civil",
  "Derecho",
  "Diseño",
  "Enfermería",
  "Estadística",
  "Filosofía",
  "Física",
  "Fonoaudiología",
  "Geografía",
  "Historia",
  "Ingeniería",
  "Ingeniería en Recursos Naturales",
  "Ingeniería Comercial",
  "Kinesiología",
  "Letras Hispánicas",
  "Letras Inglesas",
  "Licenciatura en Ingeniería en Ciencia De Datos",
  "Licenciatura en Ingeniería en Ciencia de la Computación",
  "Licenciatura en Interpretación Musical",
  "Matemática",
  "Medicina",
  "Medicina Veterinaria",
  "Música",
  "Nutrición y Dietética",
  "Odontología",
  "Pedagogía en Educación Especial",
  "Pedagogía en Educación Física y Salud",
  "Pedagogía en Educación Media en Ciencias Naturales y Biología",
  "Pedagogía en Educación Media en Física",
  "Pedagogía en Educacion Media en Matemática",
  "Pedagogía en Educación Media en Química",
  "Pedagogía en Educación Parvularia",
  "Pedagogía en Inglés",
  "Pedagogía General Básica",
  "Periodismo – Dirección Audiovisual – Publicidad",
  "Psicología",
  "Química",
  "Química y Farmacia",
  "Sociología",
  "Teología",
  "Terapia Ocupacional",
  "Trabajo Social"
]

class Rate(BaseModel):
    rating: bool  # Booleano para que sea como bueno o malo (True = bueno, False = malo)
    comment: str  # Comentario de la reseña
    profesor: str
    year: int
    semestre: int | str
    user_id: Any  # ID del usuario que dejó la reseña
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

class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    career: str
    admission_year: int

    @field_validator("admission_year")
    def check_year(cls, year: int):
        if len(str(year)) != 4:
            raise ValueError("Año no corresponde")
        return year
    @field_validator('email')
    def check_email_domain(cls, email: EmailStr):
        if not (email.endswith('@uc.cl') or email.endswith('.uc.cl')):
            raise ValueError('Email Inválido. Tu email no es UC.')
        return email
    @field_validator('career')
    def check_career(cls, career: str):
        if career not in carreras:
            raise ValueError('Carrera inválida')
        return career
    @field_validator('name')
    def check_name(cls, name: str):
        if len(name) < 3:
            raise ValueError('El nombre tiene que tener más de 3 caracteres')
        return name