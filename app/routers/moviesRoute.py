from fastapi import APIRouter
from app.controllers.moviesController import movie_router

routerMovie = APIRouter()
routerMovie.include_router(movie_router)
