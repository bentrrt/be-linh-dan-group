"""Aggregates all v1 route modules into a single router."""

from fastapi import APIRouter

from app.api.v1.routes import (
    agri_drugs,
    crop_types,
    farm_visits,
    farmers,
    farming_periods,
    farming_stage,
    land_plots,
    media,
    qr,
    reporting,
    roles,
    users,
    yield_reports,
)

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(roles.router)
# QR router must be registered before the farmers router so that the static
# path /farmers/qr is matched before the dynamic /farmers/{farmer_id}.
api_router.include_router(qr.router)
api_router.include_router(farmers.router)
api_router.include_router(land_plots.router)
api_router.include_router(crop_types.router)
api_router.include_router(agri_drugs.router)
api_router.include_router(farming_periods.router)
api_router.include_router(yield_reports.router)
api_router.include_router(farming_stage.router)
api_router.include_router(farm_visits.router)
api_router.include_router(media.router)
api_router.include_router(reporting.router)
