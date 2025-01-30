from dotenv import load_dotenv
import os


load_dotenv()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

assert POSTGRES_USER is not None, "Environment variable POSTGRES_USER is not set."
assert POSTGRES_PASSWORD is not None, "Environment variable POSTGRES_PASSWORD is not set."
assert POSTGRES_DB is not None, "Environment variable POSTGRES_DB is not set."
assert POSTGRES_HOST is not None, "Environment variable POSTGRES_HOST is not set."
assert POSTGRES_PORT is not None, "Environment variable POSTGRES_PORT is not set."
