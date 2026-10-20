from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.ventas import schemas, service

router = APIRouter(prefix="/ventas", tags=["ventas"])


def _to_read(venta):
    return schemas.VentaRead(
        id=venta.id,
        fecha=venta.fecha.isoformat(),
        total=venta.total,
        cliente={"id": venta.cliente.id, "nombre": venta.cliente.nombre, "email": venta.cliente.email},
        renglones=[
            schemas.RenglonRead(
                libro_id=r.libro_id,
                titulo=r.libro.titulo,
                cantidad=r.cantidad,
                precio_unitario=r.precio_unitario,
                subtotal=r.precio_unitario * r.cantidad,
            )
            for r in venta.renglones
        ],
    )


@router.post("/", response_model=schemas.VentaRead, status_code=201)
async def create(payload: schemas.VentaCreate, bg: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    try:
        venta = await service.create_venta(db, payload, bg)
    except ValueError as e:
        msg = str(e)
        if "duplicado" in msg:
            raise HTTPException(status_code=422, detail=msg)
        if "inexistente" in msg:
            raise HTTPException(status_code=404, detail=msg)
        if "stock insuficiente" in msg:
            raise HTTPException(status_code=409, detail=msg)
        raise HTTPException(status_code=422, detail=msg)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Error de integridad")
    return _to_read(venta)


@router.get("/", response_model=list[schemas.VentaRead])
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
):
    items = await service.list_ventas(db, limit, offset)
    return [_to_read(v) for v in items]


@router.get("/{venta_id}", response_model=schemas.VentaRead)
async def get_(venta_id: int, db: AsyncSession = Depends(get_session)):
    venta = await service.get_venta(db, venta_id)
    if venta is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return _to_read(venta)
