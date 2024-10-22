from pydantic import BaseModel

class Ramo(BaseModel):
    name: str
    code: str

class Rate(BaseModel):
    ramo_id: str
    rating: str
