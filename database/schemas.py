from pydantic import BaseModel

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str

class Rate(BaseModel):
    ramo_id: str
    rating: str
