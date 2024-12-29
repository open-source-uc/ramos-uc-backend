from pydantic import BaseModel
from random import randint

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str

class Rate(BaseModel):
    ramo_id: str
    rating: str

class Login(BaseModel):
    email: str
    pswrd: str