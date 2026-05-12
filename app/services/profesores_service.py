from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db_models import ProfesorDB
from app.models import ProfesorCreate, ProfesorUpdate


class ProfesoresService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_profesores(self) -> list[ProfesorDB]:
        return self.db.query(ProfesorDB).all()

    def get_profesor(self, profesor_id: int) -> ProfesorDB:
        profesor = self.db.get(ProfesorDB, profesor_id)
        if profesor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
        return profesor

    def create_profesor(self, profesor: ProfesorCreate) -> ProfesorDB:
        db_profesor = ProfesorDB(
            numero_empleado=profesor.numeroEmpleado,
            nombres=profesor.nombres,
            apellidos=profesor.apellidos,
            horas_clase=profesor.horasClase,
        )
        self.db.add(db_profesor)
        self.db.commit()
        self.db.refresh(db_profesor)
        return db_profesor

    def update_profesor(self, profesor_id: int, profesor: ProfesorUpdate) -> ProfesorDB:
        db_profesor = self.get_profesor(profesor_id)
        db_profesor.numero_empleado = profesor.numeroEmpleado
        db_profesor.nombres = profesor.nombres
        db_profesor.apellidos = profesor.apellidos
        db_profesor.horas_clase = profesor.horasClase
        self.db.commit()
        self.db.refresh(db_profesor)
        return db_profesor

    def delete_profesor(self, profesor_id: int) -> dict[str, str]:
        db_profesor = self.get_profesor(profesor_id)
        self.db.delete(db_profesor)
        self.db.commit()
        return {"message": "Profesor eliminado"}
