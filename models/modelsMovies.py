from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from bson import ObjectId


class MoviesModel(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    autor: str = Field(...)
    descripcion: str = Field(...)
    fecha_estreno: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "autor": "Jane Doe",
                "descripcion": "the revenge of 5 against 1",
                "fecha_estreno": "01-12-1900",
            }
        },
    )


class UpdateMovieModel(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    autor: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_estreno: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "autor": "Jane Doe",
                "descripcion": "the revenge of 5 against 1",
                "fecha_estreno": "01-12-1900",
            }
        },
    )


class MoviesCollection(BaseModel):
    movies: List[MoviesModel]
