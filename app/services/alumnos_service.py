from fastapi import HTTPException, status

from app.models import Alumno
from app.repositories.in_memory import InMemoryRepository


class AlumnosService:
    def __init__(self, repository: InMemoryRepository[Alumno]) -> None:
        self.repository = repository

    def list_alumnos(self) -> list[Alumno]:
        return self.repository.list_all()

    def get_alumno(self, alumno_id: int) -> Alumno:
        alumno = self.repository.get_by_id(alumno_id)
        if alumno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
        return alumno

    def create_alumno(self, alumno: Alumno) -> Alumno:
        existing = self.repository.get_by_id(alumno.id)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El alumno ya existe")
        return self.repository.create(alumno)

    def update_alumno(self, alumno_id: int, alumno: Alumno) -> Alumno:
        self.get_alumno(alumno_id)
        updated_alumno = alumno.model_copy(update={"id": alumno_id})
        self.repository.update(alumno_id, updated_alumno)
        return updated_alumno

    def delete_alumno(self, alumno_id: int) -> dict[str, str]:
        deleted = self.repository.delete(alumno_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
        return {"message": "Alumno eliminado"}
