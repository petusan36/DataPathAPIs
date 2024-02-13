from fastapi import APIRouter
from controllers.movies_controllers import movie_router

routerMovie = APIRouter()
routerMovie.include_router(movie_router)
