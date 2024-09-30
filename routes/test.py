from fastapi import (
    APIRouter,
    HTTPException
)
from fastapi.responses import JSONResponse, Response
from database.database import test_collection
from database.schemas import CrearCurso, VotoCurso
from bson import ObjectId
router = APIRouter()


@router.get("/")
async def obtener_curso(sigla: str, profesor: str):

    busqueda = list(test_collection.find({"sigla": sigla}))
    busqueda = list(map(lambda x: {**x, "_id": str(x["_id"])}, busqueda))
    return JSONResponse(content={"resultado": busqueda})


@router.post("/")
async def crear_curso(curso: CrearCurso):
    test_collection.insert_one(dict(curso))
    
    return JSONResponse(content={"message": "ok"})


@router.patch("/")
async def actualizar_curso(voto: VotoCurso):
    curso = test_collection.find_one({
        "_id": ObjectId(voto.id)
    })
    if curso is None:
        raise HTTPException(404, detail="No encontrado")

    curso = CrearCurso(**curso)
    if voto.valor < 0:
        curso.votos_negativos += 1
    elif voto.valor == 0:
        curso.votos_neutros += 1
    else:
         curso.votos_positivos += 1
    print(dict(curso))
    test_collection.update_one({
        "_id": ObjectId(voto.id)
    }, {"$set": dict(curso)})

    return JSONResponse(content={"message": "ok"})

@router.delete("/")
async def actualizar_curso(id: str):
    curso = test_collection.delete_one({
        "_id": ObjectId(id)
    })
    if curso is None:
        raise HTTPException(404, detail="No encontrado")


    return JSONResponse(content={"message": "ok"})

