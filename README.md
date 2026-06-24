# Asparagus Management — Backend API

FastAPI + SQLAlchemy REST API for the asparagus growing-area management and
traceability system. It connects to the PostgreSQL database defined in
`../Database/Docker/docker-compose.yml` over the shared Docker network.

## Stack

- Python 3.13, FastAPI, Uvicorn
- SQLAlchemy 2.0 ORM + Alembic migrations
- psycopg (v3) driver
- Managed with `uv`

## Project layout

```
app/
  main.py              FastAPI app, /health, CORS, router mounting
  core/                config (env) + database engine/session
  models/              ORM models mirroring the 12 existing tables
  schemas/             Pydantic request/response models
  crud/                generic CRUD base, per-model instances, reporting queries
  api/v1/routes/       endpoint modules (one per resource / FR group)
alembic/               migration environment
```

## Configuration

Copy `.env.example` to `.env` and adjust if needed. Inside Docker the DB host
is `postgres`; for local runs against the published port use `localhost`.

## Run with Docker (shared network)

The database stack must be running first:

```bash
cd ../Database/Docker && docker compose up -d
```

Then start the backend (joins the external network `docker_Asparagus_network`):

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs — health: http://localhost:8000/health

## Run locally

```bash
uv sync
DB_HOST=localhost uv run uvicorn app.main:app --reload
```

## Database migrations (Alembic)

The schema already exists (created from the raw SQL). To adopt Alembic without
recreating tables, generate a baseline and stamp the live DB:

```bash
uv run alembic revision --autogenerate -m "baseline existing schema"
uv run alembic stamp head
```

Future changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

## Endpoint ↔ functional-requirement map

| FR | Endpoint(s) |
|----|-------------|
| FR-01 | `/api/v1/users`, `/api/v1/roles`, `/api/v1/users/roles/assign` |
| FR-02 | `POST /api/v1/farmers`, `/api/v1/land-plots`, `/api/v1/farming-periods` |
| FR-03 | `POST /api/v1/reports/yield` |
| FR-04 | `GET /api/v1/reporting/yield?report_date=` |
| FR-05 | `POST /api/v1/reports/farming-stage` |
| FR-06 | `GET /api/v1/reporting/harvest-rest?date_from=&date_to=` |
| FR-07 | `GET /api/v1/farmers/{id}`, `GET /api/v1/farmers/{id}/media` |
| FR-08 | `POST /api/v1/reports/farm-visit` (+ `/reports/media`, `/reports/drug-applications`) |
| FR-09 | `GET /api/v1/farmers/qr` |
| FR-10 | `gps_lat`/`gps_long`/`submitted_mac_address` captured on report creation |
| FR-11 | `GET /api/v1/reporting/farm-visits` |
