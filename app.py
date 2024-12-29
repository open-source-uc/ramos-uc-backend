from fastapi import FastAPI
from routes import ramos_global, ratings, login

app = FastAPI()
app.include_router(login.router)
app.include_router(ramos_global.router)
app.include_router(ratings.router)