from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional


class GeneroCreate(BaseModel):
    nombre: str


class GeneroRead(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)
