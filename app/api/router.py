from fastapi import APIRouter

from app.api.routes.alumnos import router as alumnos_router
from app.api.routes.profesores import router as profesores_router

api_router = APIRouter()
api_router.include_router(alumnos_router)
api_router.include_router(profesores_router)
