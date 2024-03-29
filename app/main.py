from fastapi import FastAPI
from app.routers.moviesRoute import routerMovie


appCollections = FastAPI(
    title="Colecciones de peliculas",
    summary="API para CRUD de colecciones de peliculas"
)
appCollections.include_router(routerMovie)
