from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Editorial, Libro
from app.modules.editoriales.schemas import EditorialCreate, EditorialUpdate
from sqlalchemy.orm import selectinload


async def create_editorial(db: AsyncSession, payload: EditorialCreate) -> Editorial:
    obj = Editorial(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_editorial(db: AsyncSession, editorial_id: int) -> Editorial | None:
    res = await db.execute(select(Editorial).where(Editorial.id == editorial_id))
    return res.scalar_one_or_none()


async def list_editoriales(db: AsyncSession, limit: int, offset: int):
    res = await db.execute(select(Editorial).limit(limit).offset(offset))
    return list(res.scalars().all())


async def update_editorial(db: AsyncSession, obj: Editorial, payload: EditorialUpdate) -> Editorial:
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def libros_de_editorial(db: AsyncSession, editorial_id: int):
    res = await db.execute(
        select(Libro)
        .options(selectinload(Libro.editorial), selectinload(Libro.genero))
        .where(Libro.editorial_id == editorial_id)
    )
    return list(res.scalars().all())
