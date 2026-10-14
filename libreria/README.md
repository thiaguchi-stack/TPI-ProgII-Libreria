# Librería API

## Requisitos
- Python 3.12+
- PostgreSQL 16

## Levantar
1. Crear entorno virtual: `python -m venv .venv`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Copiar `env.example` a `.env` y configurar `DATABASE_URL`
4. Migraciones: `alembic upgrade head`
5. Servidor: `uvicorn app.main:app --reload`
