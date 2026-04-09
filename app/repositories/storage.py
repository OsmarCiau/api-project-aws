from app.models import Alumno, Profesor
from app.repositories.in_memory import InMemoryRepository

alumnos_repository = InMemoryRepository[Alumno]()
profesores_repository = InMemoryRepository[Profesor]()
