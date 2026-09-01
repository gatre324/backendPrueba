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

## Despliegue en Railway

1. Crea un servicio desde este proyecto y configura `SI2-backend` como **Root Directory**.
2. En Railway, abre **Variables** y pega el contenido de `.env.production`.
3. Reemplaza `DATABASE_POOL_URL` con la URL de Supabase. Codifica los caracteres reservados de la contraseña (`&` como `%26`, por ejemplo).
4. Reemplaza `<FRONTEND_DOMAIN>` por el dominio público del frontend Angular. Si todavía no existe, puedes dejar temporalmente `http://localhost:4200`.
5. Haz el deploy. `railway.toml` configura Railpack, ejecuta `alembic upgrade head` como pre-deploy y arranca Uvicorn en el puerto asignado por Railway.

La URL pública quedará disponible en `https://<RAILWAY_PUBLIC_DOMAIN>`. Usa esa URL como base de la API en las variables de producción de Angular y Flutter, añadiendo `/api/v1`.
