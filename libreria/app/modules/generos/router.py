from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.generos import schemas, service

router = APIRouter(prefix="/generos", tags=["generos"])


@router.post("/", response_model=schemas.GeneroRead, status_code=201)
async def create(payload: schemas.GeneroCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await service.create_genero(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/", response_model=list[schemas.GeneroRead])
async def list_(db: AsyncSession = Depends(get_session)):
    return await service.list_generos(db)


@router.get("/{genero_id}/libros")
async def libros(genero_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_genero(db, genero_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return await service.libros_de_genero(db, genero_id)
