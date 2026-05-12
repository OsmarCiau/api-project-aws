from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db_models import AlumnoDB
from app.models import AlumnoCreate, AlumnoUpdate


class AlumnosService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_alumnos(self) -> list[AlumnoDB]:
        return self.db.query(AlumnoDB).all()

    def get_alumno(self, alumno_id: int) -> AlumnoDB:
        alumno = self.db.get(AlumnoDB, alumno_id)
        if alumno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
        return alumno

    def create_alumno(self, alumno: AlumnoCreate) -> AlumnoDB:
        db_alumno = AlumnoDB(
            nombres=alumno.nombres,
            apellidos=alumno.apellidos,
            matricula=alumno.matricula,
            promedio=alumno.promedio,
            password=alumno.password,
        )
        self.db.add(db_alumno)
        self.db.commit()
        self.db.refresh(db_alumno)
        return db_alumno

    def update_alumno(self, alumno_id: int, alumno: AlumnoUpdate) -> AlumnoDB:
        db_alumno = self.get_alumno(alumno_id)
        db_alumno.nombres = alumno.nombres
        db_alumno.apellidos = alumno.apellidos
        db_alumno.matricula = alumno.matricula
        db_alumno.promedio = alumno.promedio
        db_alumno.password = alumno.password
        self.db.commit()
        self.db.refresh(db_alumno)
        return db_alumno

    def delete_alumno(self, alumno_id: int) -> dict[str, str]:
        db_alumno = self.get_alumno(alumno_id)
        self.db.delete(db_alumno)
        self.db.commit()
        return {"message": "Alumno eliminado"}
