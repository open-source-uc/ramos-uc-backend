import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.test import router as test

load_dotenv()


ORIGINS = os.environ.get("ORIGINS", None)
ORIGINS = ["localhost"] if ORIGINS is None else ORIGINS.split(",")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test, prefix="/test")
