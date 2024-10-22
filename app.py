from fastapi import FastAPI
from routes import ramos

app = FastAPI()

app.include_router(ramos.router)
