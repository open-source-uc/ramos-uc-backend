from sqlalchemy import create_engine, text
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)


def get_db():
    """Devuelve una conexión a la base de datos."""
    return engine.connect()

def execute_script_sql(archivo_sql):

    with get_db() as connection:
        with open(archivo_sql, 'r') as file:
            script_sql = file.read()
            connection.execute(text(script_sql))
            connection.commit()
            print(f"El script '{archivo_sql}' se ha ejecutado correctamente.")