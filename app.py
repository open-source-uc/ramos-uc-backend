from fastapi import FastAPI
from routes import ramos_global

app = FastAPI()

app.include_router(ramos_global.router)
