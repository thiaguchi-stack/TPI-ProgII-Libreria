from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.autores import schemas, service

router = APIRouter(prefix="/autores", tags=["autores"])


@router.post("/", response_model=schemas.AutorRead, status_code=201)
async def create(payload: schemas.AutorCreate, db: AsyncSession = Depends(get_session)):
    return await service.create_autor(db, payload)


@router.get("/{autor_id}", response_model=schemas.AutorRead)
async def get_(autor_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_autor(db, autor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.patch("/{autor_id}", response_model=schemas.AutorRead)
async def patch_(autor_id: int, payload: schemas.AutorUpdate, db: AsyncSession = Depends(get_session)):
    obj = await service.get_autor(db, autor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return await service.update_autor(db, obj, payload)


@router.get("/{autor_id}/libros")
async def libros(autor_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_autor(db, autor_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return await service.libros_de_autor(db, autor_id)
