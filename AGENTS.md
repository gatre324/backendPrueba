# SI2 Backend

## Propósito

API para la plataforma SI2 Nutricionista. En la primera vertical implementa CU-01 registro, CU-02 login y CU-04 logout.

## Stack y arquitectura

- Python 3.13 objetivo; compatible con Python 3.12 durante desarrollo.
- FastAPI, SQLAlchemy 2, Pydantic v2, Alembic, Psycopg y PostgreSQL/Supabase.
- Modular Monolith con Clean Architecture pragmática, Repository Pattern y Use Cases.
- La API pública usa `/api/v1`.
- Angular y Flutter son clientes HTTP; solo este repositorio accede a PostgreSQL.

Los routers deben ser delgados. La lógica vive en `application/use_cases`, el dominio no depende de FastAPI y el acceso a datos pasa por repositories.

## Seguridad y datos

- Contraseñas siempre con `pwdlib`/Argon2; nunca guardar ni devolver texto plano o `password_hash`.
- JWT Bearer de acceso con expiración; no colocar secretos en clientes.
- El usuario inactivo no puede iniciar sesión.
- No confiar en `tenant_id` enviado por el cliente; la futura autorización debe derivarse del usuario autenticado.
- `.env` nunca debe subirse a Git. La contraseña actual fue expuesta durante configuración y debe rotarse.
- El backend usa Transaction Pooler en desarrollo; Session/Direct Pooler es preferible para migraciones y producción persistente.

## Comandos

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
pytest
```

Para red local: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.

## Agregar features

Crear un módulo en `app/modules/<feature>` con domain, application, infrastructure y api. Añadir modelos a `Base.metadata`, una migración Alembic, use cases, repository, router y pruebas. Mantener contratos JSON en `snake_case`.

## Estado

Implementados: usuarios, registro público como paciente, login JWT, `/me`, logout stateless, health check y migración inicial. Pendientes: confirmación SMTP real, refresh/revocación de tokens, tenants, organizaciones, permisos y funcionalidades nutricionales.
