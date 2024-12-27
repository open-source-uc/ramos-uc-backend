from fastapi import FastAPI
from routes import ramos_global, ratings

app = FastAPI()

app.include_router(ramos_global.router)
app.include_router(ratings.router)