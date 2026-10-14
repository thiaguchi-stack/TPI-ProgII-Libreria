from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Genero, Libro
from app.modules.generos.schemas import GeneroCreate
from sqlalchemy.orm import selectinload


async def create_genero(db, payload):
    obj = Genero(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def list_generos(db):
    res = await db.execute(select(Genero))
    return list(res.scalars().all())


async def get_genero(db, genero_id):
    res = await db.execute(select(Genero).where(Genero.id == genero_id))
    return res.scalar_one_or_none()


async def libros_de_genero(db, genero_id):
    res = await db.execute(select(Libro).options(selectinload(Libro.editorial), selectinload(Libro.genero)).where(Libro.genero_id == genero_id))
    return list(res.scalars().all())
