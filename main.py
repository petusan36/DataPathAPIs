from fastapi import FastAPI
from routers.routerMovies import routerMovie


appCollections = FastAPI(
    title="Colecciones de peliculas",
    summary="API para CRUD de colecciones de peliculas"
)
appCollections.include_router(routerMovie)
