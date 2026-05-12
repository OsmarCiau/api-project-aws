from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlumnoDB(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombres: Mapped[str] = mapped_column(String(200), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(200), nullable=False)
    matricula: Mapped[str] = mapped_column(String(100), nullable=False)
    promedio: Mapped[float] = mapped_column(Float, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    foto_perfil_url: Mapped[str | None] = mapped_column(String(500), nullable=True)


class ProfesorDB(Base):
    __tablename__ = "profesores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    nombres: Mapped[str] = mapped_column(String(200), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(200), nullable=False)
    horas_clase: Mapped[int] = mapped_column(Integer, nullable=False)
