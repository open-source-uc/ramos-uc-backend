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
#User
class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    career: str
    admission_year: str

    @field_validator("admission_year")
    def check_year(self, year: int):
        if len(str(year)) != 4:
            raise ValueError("Año no corresponde")
        return year
    @field_validator('email')
    def check_email_domain(self, email: EmailStr):
        if not email.endswith('@uc.cl') or not email.endswith('@estudiante.uc.cl'):
            raise ValueError('Email Inválido. Tu email no es UC.')
        return email
    @field_validator('career')
    def check_career(self, career: str):
        if career not in carreras:
            raise ValueError('Carrera inválida')
        return career