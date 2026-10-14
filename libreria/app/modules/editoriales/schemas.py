from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional


class EditorialCreate(BaseModel):
    nombre: str
    pais: Optional[str] = None


class EditorialUpdate(BaseModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None


class EditorialRead(BaseModel):
    id: int
    nombre: str
    pais: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
