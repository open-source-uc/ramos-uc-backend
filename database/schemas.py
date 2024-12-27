from pydantic import BaseModel

class Ramo(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str

class Rate(BaseModel):
    ramo_id: str
    rating: bool #Booleano para que sea como bueno o malo despues se sacan los promedios
    comment: str #Maybe agruegar longitud maxima dsp
    user_id: str #Esto para identificar de que cuenta es cada comentario moderación etc