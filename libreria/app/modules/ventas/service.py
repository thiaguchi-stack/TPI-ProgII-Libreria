from __future__ import annotations

import asyncio
import logging
from decimal import Decimal
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Libro, RenglonVenta, Venta

logger = logging.getLogger(__name__)


async def enviar_comprobante(cliente_id: int, venta_id: int) -> None:
    await asyncio.sleep(0.5)
    logger.info("Comprobante enviado para venta %s al cliente %s", venta_id, cliente_id)


async def get_venta(db: AsyncSession, venta_id: int):
    res = await db.execute(
        select(Venta)
        .options(
            selectinload(Venta.cliente),
            selectinload(Venta.renglones).selectinload(RenglonVenta.libro),
        )
        .where(Venta.id == venta_id)
    )
    return res.scalar_one_or_none()


async def list_ventas(db: AsyncSession, limit: int, offset: int):
    res = await db.execute(
        select(Venta)
        .options(selectinload(Venta.cliente), selectinload(Venta.renglones))
        .limit(limit)
        .offset(offset)
    )
    return list(res.scalars().all())


async def create_venta(db: AsyncSession, payload, background_tasks):
    if len({r.libro_id for r in payload.renglones}) != len(payload.renglones):
        raise ValueError("libro duplicado en renglones")

    libro_ids = [r.libro_id for r in payload.renglones]
    res = await db.execute(select(Libro).where(Libro.id.in_(libro_ids)))
    libros = {l.id: l for l in res.scalars().all()}
    if len(libros) != len(set(libro_ids)):
        raise ValueError("libro inexistente")

    venta = Venta(cliente_id=payload.cliente_id, total=Decimal("0.00"))
    db.add(venta)
    await db.flush()

    total = Decimal("0.00")
    for r in payload.renglones:
        libro = libros[r.libro_id]
        precio = libro.precio
        subtotal = precio * r.cantidad
        total += subtotal
        db.add(
            RenglonVenta(
                venta_id=venta.id,
                libro_id=r.libro_id,
                cantidad=r.cantidad,
                precio_unitario=precio,
            )
        )
    venta.total = total
    db.add(venta)
    await db.commit()

    if background_tasks is not None:
        background_tasks.add_task(enviar_comprobante, payload.cliente_id, venta.id)
    return await get_venta(db, venta.id)
