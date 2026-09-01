# SI2 Nutricionista Backend

API FastAPI para Angular y Flutter. PostgreSQL está alojado en Supabase y es accedido exclusivamente por este servicio.

## Requisitos

Python 3.12+ (objetivo 3.13), PostgreSQL/Supabase y Git.

## Configuración

Copiar `.env.example` a `.env` y completar `DATABASE_POOL_URL` y `JWT_SECRET_KEY`. La contraseña debe codificarse en URL (`&` como `%26`, por ejemplo). Nunca compartir ni versionar `.env`.

## Ejecución

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Documentación: `http://localhost:8000/docs`. Health: `http://localhost:8000/health`.

## Endpoints actuales

`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`.

## Pruebas

```powershell
pytest
```

La arquitectura es modular, basada en repositories y use cases; no usar MVC clásico ni acceder a la base desde los clientes.
