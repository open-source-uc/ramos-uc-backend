from pydantic import BaseModel, ValidationError, field_validator, Field, EmailStr

class CrearCurso(BaseModel):
    sigla: str
    profesor: str
    votos_positivos: int
    votos_neutros: int
    votos_negativos: int

class VotoCurso(BaseModel):
    valor: int
    id: str

