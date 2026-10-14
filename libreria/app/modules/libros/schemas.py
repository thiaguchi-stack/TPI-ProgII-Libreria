from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class LibroAutorCreate(BaseModel):
    autor_id: int
    rol: str = "autor"
    orden: int = 1


class LibroCreate(BaseModel):
    isbn: str
    titulo: str
    precio: Decimal
    stock: int = 0
    editorial_id: int
    genero_id: Optional[int] = None
    autores: List[LibroAutorCreate] = []


class LibroUpdate(BaseModel):
    isbn: Optional[str] = None
    titulo: Optional[str] = None
    precio: Optional[Decimal] = None
    stock: Optional[int] = None
    editorial_id: Optional[int] = None
    genero_id: Optional[int] = None


class EditorialMini(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class GeneroMini(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class AutorMini(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class AutoriaRead(BaseModel):
    autor: AutorMini
    rol: str
    orden: int

    model_config = ConfigDict(from_attributes=True)


class LibroRead(BaseModel):
    id: int
    isbn: str
    titulo: str
    precio: Decimal
    stock: int
    editorial_id: int
    genero_id: Optional[int] = None
    editorial: Optional[EditorialMini] = None
    genero: Optional[GeneroMini] = None
    autores: List[AutoriaRead] = []

    model_config = ConfigDict(from_attributes=True)
