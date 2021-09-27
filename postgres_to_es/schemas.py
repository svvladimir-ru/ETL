from uuid import UUID

from datetime import datetime
from typing import Union, Optional, List
from pydantic import BaseModel, Field


class DSNSettings(BaseModel):
    host: str
    port: int
    dbname: str
    password: str
    user: str


class PostgresSettings(BaseModel):
    dsn: DSNSettings
    limit: Optional[int]
    order_field: List[str]
    state_field: List[str]
    fetch_delay: Optional[float]
    state_file_path: Optional[str]
    sql_query: str


class Config(BaseModel):
    film_work_pg: PostgresSettings


config = Config.parse_file('config.json')

print(config.film_work_pg.dsn.user)


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