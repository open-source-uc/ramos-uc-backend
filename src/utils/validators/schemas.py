from pydantic import BaseModel


class CourseSchema(BaseModel):
    sigle: str
    name: str
    credits: int
    school: str
    area: str
    category: str

    class Config:
        orm_mode = True