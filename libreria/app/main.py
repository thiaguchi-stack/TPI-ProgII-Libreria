from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa
from app.core.database import create_engine_and_session_factory
from app.modules.health.router import router as health_router
from app.modules.editoriales.router import router as editoriales_router
from app.modules.generos.router import router as generos_router
from app.modules.autores.router import router as autores_router
from app.modules.libros.router import router as libros_router
from app.modules.clientes.router import router as clientes_router
from app.modules.ventas.router import router as ventas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine, session_factory = create_engine_and_session_factory()
    app.state.engine = engine
    app.state.session_factory = session_factory
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(editoriales_router)
app.include_router(generos_router)
app.include_router(autores_router)
app.include_router(libros_router)
app.include_router(clientes_router)
app.include_router(ventas_router)