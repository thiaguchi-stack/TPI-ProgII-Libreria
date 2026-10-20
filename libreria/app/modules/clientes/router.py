from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.clientes import schemas, service
from app.modules.ventas import schemas as vschemas

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=schemas.ClienteRead, status_code=201)
async def create(payload: schemas.ClienteCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await service.create_cliente(db, payload)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/{cliente_id}", response_model=schemas.ClienteRead)
async def get_(cliente_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_cliente(db, cliente_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.patch("/{cliente_id}", response_model=schemas.ClienteRead)
async def patch_(cliente_id: int, payload: schemas.ClienteUpdate, db: AsyncSession = Depends(get_session)):
    obj = await service.get_cliente(db, cliente_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    try:
        return await service.update_cliente(db, obj, payload)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.post("/{cliente_id}/perfil", response_model=schemas.PerfilRead, status_code=201)
async def perfil(cliente_id: int, payload: schemas.PerfilCreate, db: AsyncSession = Depends(get_session)):
    cli = await service.get_cliente(db, cliente_id)
    if cli is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    if cli.perfil is not None:
        raise HTTPException(status_code=409, detail="Perfil existente")
    try:
        return await service.crear_perfil(db, cliente_id, payload)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/{cliente_id}/ventas", response_model=list[vschemas.VentaResumen])
async def ventas(cliente_id: int, db: AsyncSession = Depends(get_session)):
    cli = await service.get_cliente(db, cliente_id)
    if cli is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return await service.ventas_de_cliente(db, cliente_id)
