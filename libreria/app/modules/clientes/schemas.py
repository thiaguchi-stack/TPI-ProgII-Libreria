from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ClienteCreate(BaseModel):
    nombre: str
    email: str


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None


class PerfilCreate(BaseModel):
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class PerfilRead(BaseModel):
    id: int
    cliente_id: int
    telefono: Optional[str] = None
    direccion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ClienteRead(BaseModel):
    id: int
    nombre: str
    email: str
    perfil: Optional[PerfilRead] = None

    model_config = ConfigDict(from_attributes=True)
