"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title="Asparagus Management API",
    version="0.1.0",
    description="REST API for the asparagus growing-area management and traceability system.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness + database connectivity check."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception as exc:  # noqa: BLE001 - report any DB failure to the caller
        return {"status": "degraded", "database": "error", "detail": str(exc)}


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"service": "asparagus-backend", "docs": "/docs"}
