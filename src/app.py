from fastapi import FastAPI
from routes import login
from database.seed import seed_data

app = FastAPI()

@app.on_event("startup")
async def lifespan():
    seed_data()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

app.include_router(login.router)
# app.include_router(ramos_global.router)
# app.include_router(ratings.router)