from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.editoriales import schemas, service

router = APIRouter(prefix="/editoriales", tags=["editoriales"])


@router.post("/", response_model=schemas.EditorialRead, status_code=201)
async def create(payload: schemas.EditorialCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await service.create_editorial(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/", response_model=list[schemas.EditorialRead])
async def list_(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_session)):
    return await service.list_editoriales(db, limit, offset)


@router.get("/{editorial_id}", response_model=schemas.EditorialRead)
async def get_(editorial_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_editorial(db, editorial_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.patch("/{editorial_id}", response_model=schemas.EditorialRead)
async def patch_(editorial_id: int, payload: schemas.EditorialUpdate, db: AsyncSession = Depends(get_session)):
    obj = await service.get_editorial(db, editorial_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    try:
        return await service.update_editorial(db, obj, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/{editorial_id}/libros")
async def libros(editorial_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_editorial(db, editorial_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return await service.libros_de_editorial(db, editorial_id)
