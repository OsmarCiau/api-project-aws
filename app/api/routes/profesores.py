from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db_models import ProfesorDB
from app.models import MessageResponse, ProfesorCreate, ProfesorOut, ProfesorUpdate
from app.services.profesores_service import ProfesoresService

router = APIRouter(prefix="/profesores", tags=["Profesores"])


@router.get("", response_model=list[ProfesorOut], status_code=status.HTTP_200_OK)
def get_profesores(db: Session = Depends(get_db)) -> list[ProfesorDB]:
    service = ProfesoresService(db)
    return service.list_profesores()


@router.get("/{id}", response_model=ProfesorOut, status_code=status.HTTP_200_OK)
def get_profesor(id: int, db: Session = Depends(get_db)) -> ProfesorDB:
    service = ProfesoresService(db)
    return service.get_profesor(id)


@router.post("", response_model=ProfesorOut, status_code=status.HTTP_201_CREATED)
def create_profesor(profesor: ProfesorCreate, db: Session = Depends(get_db)) -> ProfesorDB:
    service = ProfesoresService(db)
    return service.create_profesor(profesor)


@router.put("/{id}", response_model=ProfesorOut, status_code=status.HTTP_200_OK)
def update_profesor(id: int, profesor: ProfesorUpdate, db: Session = Depends(get_db)) -> ProfesorDB:
    service = ProfesoresService(db)
    return service.update_profesor(id, profesor)


@router.delete("/{id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_profesor(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    service = ProfesoresService(db)
    return service.delete_profesor(id)
