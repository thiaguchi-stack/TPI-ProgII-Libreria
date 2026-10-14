from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Autor, Libro, LibroAutor
from app.modules.autores.schemas import AutorCreate, AutorUpdate
from sqlalchemy.orm import selectinload


async def create_autor(db, payload):
    obj = Autor(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_autor(db, autor_id):
    res = await db.execute(select(Autor).where(Autor.id == autor_id))
    return res.scalar_one_or_none()


async def update_autor(db, obj, payload):
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def libros_de_autor(db, autor_id):
    # libros con rol y orden
    res = await db.execute(
        select(LibroAutor, Libro)
        .join(Libro)
        .where(LibroAutor.autor_id == autor_id)
        .options(selectinload(LibroAutor.libro).selectinload(Libro.editorial))
    )
    out = []
    for la, libro in res.all():
        out.append((libro, la.rol, la.orden))
    return out
