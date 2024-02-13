from fastapi import APIRouter, HTTPException, status, Body
from models.modelsMovies import MoviesCollection, MoviesModel, UpdateMovieModel
from mongoDB.mongo_connect import movies_collection, counters_collection
from fastapi.responses import Response
from pymongo import ReturnDocument

movie_router = APIRouter()


@movie_router.get(
    "/",
    tags=["/"],
    response_description="Mensaje Bienvenida",
)
async def read_root():
    """
    Bienvenid@ a la API
    """
    return {"message": "App de lista de peliculas en colección"}


@movie_router.get(
    "/movies/",
    tags=["Listar peliculas en Colección"],
    response_description="Lista de peliculas en colección",
    response_model=MoviesCollection,
    response_model_by_alias=False,
)
async def list_movies():
    """
    Lista todas las peliculas
    Sin paginar y limitada a `1000` resultados.
    """
    return MoviesCollection(movies=await movies_collection.find().to_list(1000))


@movie_router.get(
    "/movies/{id}",
    tags=["Listar peliculas en colección por Id"],
    response_description="Pelicula de la colección",
    response_model=MoviesModel,
    response_model_by_alias=False,
)
async def show_movie(id_movie: int):
    """
    Devuelve un registro especifico buscado por `Id`.
    """
    if (
        movie := await movies_collection.find_one({"_id": id_movie})
    ) is not None:
        return movie

    raise HTTPException(status_code=404, detail=f"Pelicula {id_movie} no encontrada")


@movie_router.post(
    "/movies/",
    tags=["Agregar peliculas en colección"],
    response_description="Pelicula agregada a la colección",
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


@movie_router.put(
    "/movies/{id}",
    tags=["Actualizar peliculas de la colección por Id"],
    response_description="Pelicula actualizada en la colección",
    response_model=MoviesModel,
    response_model_by_alias=False,
)
async def update_movie(id_movie: int, movie: UpdateMovieModel = Body(...)):
    """
    Actualiza un campo de manera individual para un registro existente

    solo los campos suministrados serán actualizados. Campos faltantes o nulos serán ignorados.
    """
    movie = {
        k: v for k, v in movie.model_dump(by_alias=True).items() if v is not None
    }

    if len(movie) >= 1:
        update_result = await movies_collection.find_one_and_update(
            {"_id": id_movie},
            {"$set": movie},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Pelicula {id_movie} no encontrada")

    # The update is empty, but we should still return the matching document:
    if (existing_movie := await movies_collection.find_one({"_id": id_movie})) is not None:
        return existing_movie

    raise HTTPException(status_code=404, detail=f"Pelicula {id_movie} no encontrada")


@movie_router.delete(
    "/movies/{id}",
    tags=["Eliminar peliculas de la colección por Id"],
    response_description="Pelicula eliminada de la colección",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(id_movie: int):
    """
    Elimina un registro de una pelicula de la base de datos
    """
    delete_result = await movies_collection.delete_one({"_id": id_movie})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Pelicula {id_movie} no encontrada")
