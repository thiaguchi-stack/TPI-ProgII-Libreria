from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Cliente, PerfilCliente, Venta


async def create_cliente(db, payload):
    obj = Cliente(**payload.model_dump())
    db.add(obj)
    await db.commit()
    return await get_cliente(db, obj.id)


async def get_cliente(db, cliente_id):
    res = await db.execute(
        select(Cliente)
        .options(selectinload(Cliente.perfil))
        .where(Cliente.id == cliente_id)
    )
    return res.scalar_one_or_none()


async def update_cliente(db, obj, payload):
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    return await get_cliente(db, obj.id)


async def crear_perfil(db, cliente_id, payload):
    obj = PerfilCliente(cliente_id=cliente_id, **payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def ventas_de_cliente(db, cliente_id):
    res = await db.execute(select(Venta).where(Venta.cliente_id == cliente_id))
    return list(res.scalars().all())
