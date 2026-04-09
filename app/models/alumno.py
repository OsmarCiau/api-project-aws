from pydantic import BaseModel, Field, field_validator


class Alumno(BaseModel):
    id: int = Field(gt=0)
    nombres: str
    apellidos: str
    matricula: str
    promedio: float = Field(ge=0.0, le=100.0)

    @field_validator("nombres", "apellidos", "matricula")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value
