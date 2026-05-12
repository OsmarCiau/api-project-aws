from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator


class AlumnoBase(BaseModel):
    nombres: StrictStr
    apellidos: StrictStr
    matricula: StrictStr
    promedio: float = Field(ge=0.0, le=100.0)
    password: StrictStr

    @field_validator("nombres", "apellidos", "matricula", "password")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value


class AlumnoCreate(AlumnoBase):
    pass


class AlumnoUpdate(AlumnoBase):
    pass


class AlumnoOut(BaseModel):
    id: int = Field(gt=0)
    nombres: str
    apellidos: str
    matricula: str
    promedio: float
    foto_perfil_url: str | None = Field(default=None, serialization_alias="fotoPerfilUrl")

    model_config = ConfigDict(from_attributes=True)
