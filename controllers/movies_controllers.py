from fastapi import APIRouter, HTTPException, status, Body
from models import MoviesCollection, MoviesModel, CounterModel, UpdateMovieModel
from MongoDB.mongo_connect import movies_collection, counters_collection
# from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()


@router.get(
    "/",
    tags=["/"],
    response_model=CounterModel,
)
async def read_root():
    """
    Bienvenida a la API
    """
    return {"message": "App de lista de peliculas en cartelera"}


@router.get(
    "/movies/",
    tags=["Listar Peliculas en Cartelera"],
    response_description="Lista de peliculas en cartelera",
    response_model=MoviesCollection,
    response_model_by_alias=False,
)
async def list_movies():
    """
    Lista tadas las peliculas
    The es sin paginar y limitada a 1000 resultados.
    """
    return MoviesCollection(movies=await movies_collection.find().to_list(1000))


@router.get(
    "/movies/{id}",
    tags=["Listar Peliculas en Cartelera por Id"],
    response_description="Lista una pelicula",
    response_model=MoviesModel,
    response_model_by_alias=False,
)
async def show_movie(id: int):
    """
    Devuelve un registro especifico buscado por `Id`.
    """
    if (
        movie := await movies_collection.find_one({"_id": id})
    ) is not None:
        return movie

    raise HTTPException(status_code=404, detail=f"Pelicula {id} no encontrada")


@router.post(
    "/movies/",
    tags=["Adicionar Peliculas en Cartelera"],
    response_description="Adiciona nuevas peliculas",
    response_model=MoviesModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_movie(movie: MoviesModel = Body(...)):
    """
    Inserta un nuevo registro de pelicula en cartelera.
    """
    counter = await counters_collection.find_one({"_id": "userid"})
    movie_n = movie.model_dump(by_alias=True)

    movie_n["_id"] = counter["seq"]+1
    counter["seq"] = counter["seq"]+1

    new_movie = await movies_collection.insert_one(
        movie_n
    )
    created_movie = await movies_collection.find_one(
        {"_id": new_movie.inserted_id}
    )

    if created_movie is not None:
        await counters_collection.find_one_and_update(
            {"_id": counter["_id"]},
            {"$set": counter})

    return created_movie


@router.put(
    "/movies/{id}",
    response_description="Actualiza una pelicula",
    response_model=MoviesModel,
    response_model_by_alias=False,
)
async def update_movie(id: int, movie: UpdateMovieModel = Body(...)):
    """
    Actualiza un campo de manera individual para un registro existente

    solo los campos suministrados serán actualizados.
    Campos faltantes o nulos serán ignorados.
    """
    movie = {
        k: v for k, v in movie.model_dump(by_alias=True).items() if v is not None
    }

    if len(movie) >= 1:
        update_result = await movies_collection.find_one_and_update(
            {"_id": id},
            {"$set": movie},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Pelicula {id} no encontrada")

    # The update is empty, but we should still return the matching document:
    if (existing_movie := await movies_collection.find_one({"_id": id})) is not None:
        return existing_movie

    raise HTTPException(status_code=404, detail=f"Pelicula {id} no encontrada")
