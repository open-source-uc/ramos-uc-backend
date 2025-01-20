from fastapi import FastAPI
# from routes import login
from contextlib import asynccontextmanager

from database.database import execute_script_sql

app = FastAPI()

@app.on_event("startup")
async def lifespan():
    execute_script_sql("./sql_query/tables.sql")
    execute_script_sql("./sql_query/inserts.sql")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# app.include_router(login.router)
# app.include_router(ramos_global.router)
# app.include_router(ratings.router)