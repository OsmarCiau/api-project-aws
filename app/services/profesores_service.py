from fastapi import HTTPException, status

from app.models import Profesor
from app.repositories.in_memory import InMemoryRepository


class ProfesoresService:
    def __init__(self, repository: InMemoryRepository[Profesor]) -> None:
        self.repository = repository

    def list_profesores(self) -> list[Profesor]:
        return self.repository.list_all()

    def get_profesor(self, profesor_id: int) -> Profesor:
        profesor = self.repository.get_by_id(profesor_id)
        if profesor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return profesor

    def create_profesor(self, profesor: Profesor) -> Profesor:
        existing = self.repository.get_by_id(profesor.id)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El profesor ya existe")
        return self.repository.create(profesor)

    def update_profesor(self, profesor_id: int, profesor: Profesor) -> Profesor:
        self.get_profesor(profesor_id)
        updated_profesor = profesor.model_copy(update={"id": profesor_id})
        self.repository.update(profesor_id, updated_profesor)
        return updated_profesor

    def delete_profesor(self, profesor_id: int) -> dict[str, str]:
        deleted = self.repository.delete(profesor_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return {"message": "Profesor eliminado"}
