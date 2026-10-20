from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class RenglonCreate(BaseModel):
    libro_id: int
    cantidad: int = Field(gt=0)


class VentaCreate(BaseModel):
    cliente_id: int
    renglones: List[RenglonCreate] = Field(min_length=1)


class RenglonRead(BaseModel):
    libro_id: int
    titulo: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class VentaRead(BaseModel):
    id: int
    fecha: str
    total: Decimal
    cliente: dict
    renglones: List[RenglonRead]

    model_config = ConfigDict(from_attributes=True)


class VentaResumen(BaseModel):
    id: int
    cliente_id: int
    fecha: datetime
    total: Decimal

    model_config = ConfigDict(from_attributes=True)
