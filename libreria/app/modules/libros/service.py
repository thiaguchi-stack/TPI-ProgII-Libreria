from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models import Libro, LibroAutor
from app.modules.libros.schemas import LibroCreate, LibroUpdate


def _opts(q):
    return q.options(
        joinedload(Libro.editorial),
        joinedload(Libro.genero),
        selectinload(Libro.autorias).selectinload(LibroAutor.autor),
    )


async def get_libro(db: AsyncSession, libro_id: int):
    res = await db.execute(_opts(select(Libro).where(Libro.id == libro_id)))
    return res.scalar_one_or_none()


async def create_libro(db: AsyncSession, payload: LibroCreate):
    libro = Libro(
        isbn=payload.isbn,
        titulo=payload.titulo,
        precio=payload.precio,
        stock=payload.stock,
        editorial_id=payload.editorial_id,
        genero_id=payload.genero_id,
    )
    db.add(libro)
    await db.flush()
    for a in payload.autores:
        db.add(
            LibroAutor(
                libro_id=libro.id,
                autor_id=a.autor_id,
                rol=a.rol,
                orden=a.orden,
            )
        )
    await db.commit()
    return await get_libro(db, libro.id)


async def list_libros(db, limit, offset, titulo=None, genero_id=None):
    q = _opts(select(Libro))
    if titulo:
        q = q.where(Libro.titulo.ilike(f"%{titulo}%"))
    if genero_id is not None:
        q = q.where(Libro.genero_id == genero_id)
    q = q.limit(limit).offset(offset)
    res = await db.execute(q)
    return list(res.scalars().unique().all())


async def update_libro(db, obj, payload: LibroUpdate):
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    return await get_libro(db, obj.id)
