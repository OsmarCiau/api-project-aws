from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator


class ProfesorBase(BaseModel):
    numeroEmpleado: StrictInt = Field(gt=0)
    nombres: StrictStr
    apellidos: StrictStr
    horasClase: StrictInt = Field(ge=0)

    @field_validator("nombres", "apellidos")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value


class ProfesorCreate(ProfesorBase):
    pass


class ProfesorUpdate(ProfesorBase):
    pass


class ProfesorOut(BaseModel):
    id: int = Field(gt=0)
    numero_empleado: int = Field(serialization_alias="numeroEmpleado")
    nombres: str
    apellidos: str
    horas_clase: int = Field(serialization_alias="horasClase")

    model_config = ConfigDict(from_attributes=True)
