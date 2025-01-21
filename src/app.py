from fastapi import FastAPI
import routes.courses.route as courses
import routes.auth.route as auth
import routes.reviews.route as reviews
import routes.user.route as user
from database.seed import seed_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.on_event("startup")
async def lifespan():
    seed_data()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!", "version": "0.0.3"}
# Router para autenticación
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Router para cursos
app.include_router(courses.router, prefix="/courses", tags=["courses"])

# Router para reseñas
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])

app.include_router(user.router, prefix="/user", tags=["user"])