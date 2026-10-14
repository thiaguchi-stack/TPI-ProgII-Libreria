from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional


class AutorCreate(BaseModel):
    nombre: str
    nacionalidad: Optional[str] = None


class AutorUpdate(BaseModel):
    nombre: Optional[str] = None
    nacionalidad: Optional[str] = None


class AutorRead(BaseModel):
    id: int
    nombre: str
    nacionalidad: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
