from fastapi import APIRouter, status

from app.models import Alumno
from app.repositories.storage import alumnos_repository
from app.services.alumnos_service import AlumnosService

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])
service = AlumnosService(alumnos_repository)


@router.get("", response_model=list[Alumno], status_code=status.HTTP_200_OK)
def get_alumnos() -> list[Alumno]:
    return service.list_alumnos()


@router.get("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def get_alumno(id: int) -> Alumno:
    return service.get_alumno(id)


@router.post("", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(alumno: Alumno) -> Alumno:
    return service.create_alumno(alumno)


@router.put("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def update_alumno(id: int, alumno: Alumno) -> Alumno:
    return service.update_alumno(id, alumno)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_alumno(id: int) -> dict[str, str]:
    return service.delete_alumno(id)
