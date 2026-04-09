from pydantic import BaseModel, Field, field_validator


class Profesor(BaseModel):
    id: int = Field(gt=0)
    numeroEmpleado: int = Field(gt=0)
    nombres: str
    apellidos: str
    horasClase: int = Field(ge=0)

    @field_validator("nombres", "apellidos")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value
