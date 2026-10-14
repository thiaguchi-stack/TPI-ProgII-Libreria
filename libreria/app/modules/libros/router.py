from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.libros import schemas, service

router = APIRouter(prefix="/libros", tags=["libros"])


@router.post("/", response_model=schemas.LibroRead, status_code=201)
async def create(payload: schemas.LibroCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await service.create_libro(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error de unicidad")


@router.get("/", response_model=list[schemas.LibroRead])
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    titulo: str | None = None,
    genero_id: int | None = None,
    db: AsyncSession = Depends(get_session),
):
    return await service.list_libros(db, limit, offset, titulo, genero_id)


@router.get("/{libro_id}", response_model=schemas.LibroRead)
async def get_(libro_id: int, db: AsyncSession = Depends(get_session)):
    obj = await service.get_libro(db, libro_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return obj


@router.patch("/{libro_id}", response_model=schemas.LibroRead)
async def patch_(libro_id: int, payload: schemas.LibroUpdate, db: AsyncSession = Depends(get_session)):
    obj = await service.get_libro(db, libro_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    try:
        return await service.update_libro(db, obj, payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Error de unicidad")
