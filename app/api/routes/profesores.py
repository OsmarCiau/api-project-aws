from fastapi import APIRouter, status

from app.models import Profesor
from app.repositories.storage import profesores_repository
from app.services.profesores_service import ProfesoresService

router = APIRouter(prefix="/profesores", tags=["Profesores"])
service = ProfesoresService(profesores_repository)


@router.get("", response_model=list[Profesor], status_code=status.HTTP_200_OK)
def get_profesores() -> list[Profesor]:
    return service.list_profesores()


@router.get("/{id}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_profesor(id: int) -> Profesor:
    return service.get_profesor(id)


@router.post("", response_model=Profesor, status_code=status.HTTP_201_CREATED)
def create_profesor(profesor: Profesor) -> Profesor:
    return service.create_profesor(profesor)


@router.put("/{id}", response_model=Profesor, status_code=status.HTTP_200_OK)
def update_profesor(id: int, profesor: Profesor) -> Profesor:
    return service.update_profesor(id, profesor)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_profesor(id: int) -> dict[str, str]:
    return service.delete_profesor(id)
