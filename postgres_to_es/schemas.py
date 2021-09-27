from uuid import UUID

from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field


class FilmWorkWithoutField(BaseModel):
    id: Union[int, str, UUID]
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    type: str
    created_at: datetime
    updated_at: datetime
    rating: float = Field(default=0.0)


class GenreWithoutField(BaseModel):
    id: Union[int, str, UUID]
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class GenreFilmWorkWithoutField(BaseModel):
    id: Union[int, str, UUID]
    film_work_id: Union[int, str, UUID]
    genre_id: Union[int, str, UUID]
    created_at: datetime


class PersonWithoutField(BaseModel):
    id: UUID
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime


class PersonFilmWorkWithoutField(BaseModel):
    film_work_id: Union[int, str, UUID]
    person_id: Union[int, str, UUID]
    role: str
    created_at: datetime
    id: Union[int, str, UUID]