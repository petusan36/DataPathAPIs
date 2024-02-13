from fastapi import FastAPI
from routes import router


app = FastAPI(
    title="Cartelera de peliculas",
    summary="API para CRUD de Cartelera de cine"
)
app.include_router(router)
