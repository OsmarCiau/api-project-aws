from pydantic import BaseModel, StrictStr, field_validator


class SessionLogin(BaseModel):
    password: StrictStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value


class SessionAction(BaseModel):
    sessionString: StrictStr

    @field_validator("sessionString")
    @classmethod
    def validate_session_string(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("No puede estar vacio")
        return value


class SessionResponse(BaseModel):
    sessionString: str


class FotoPerfilResponse(BaseModel):
    fotoPerfilUrl: str


class MessageResponse(BaseModel):
    message: str
