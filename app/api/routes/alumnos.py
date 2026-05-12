import secrets

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.aws import (
    create_session_item,
    deactivate_session_item,
    find_session_item,
    publish_alumno_email,
    upload_profile_picture,
)
from app.db import get_db
from app.db_models import AlumnoDB
from app.models import (
    AlumnoCreate,
    AlumnoOut,
    AlumnoUpdate,
    FotoPerfilResponse,
    MessageResponse,
    SessionAction,
    SessionLogin,
    SessionResponse,
)
from app.services.alumnos_service import AlumnosService

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.get("", response_model=list[AlumnoOut], status_code=status.HTTP_200_OK)
def get_alumnos(db: Session = Depends(get_db)) -> list[AlumnoDB]:
    service = AlumnosService(db)
    return service.list_alumnos()


@router.get("/{id}", response_model=AlumnoOut, status_code=status.HTTP_200_OK)
def get_alumno(id: int, db: Session = Depends(get_db)) -> AlumnoDB:
    service = AlumnosService(db)
    return service.get_alumno(id)


@router.post("", response_model=AlumnoOut, status_code=status.HTTP_201_CREATED)
def create_alumno(alumno: AlumnoCreate, db: Session = Depends(get_db)) -> AlumnoDB:
    service = AlumnosService(db)
    return service.create_alumno(alumno)


@router.put("/{id}", response_model=AlumnoOut, status_code=status.HTTP_200_OK)
def update_alumno(id: int, alumno: AlumnoUpdate, db: Session = Depends(get_db)) -> AlumnoDB:
    service = AlumnosService(db)
    return service.update_alumno(id, alumno)


@router.delete("/{id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_alumno(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    service = AlumnosService(db)
    return service.delete_alumno(id)


@router.post("/{id}/fotoPerfil", response_model=FotoPerfilResponse, status_code=status.HTTP_200_OK)
def upload_foto_perfil(
    id: int,
    foto: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> FotoPerfilResponse:
    service = AlumnosService(db)
    alumno = service.get_alumno(id)
    url = upload_profile_picture(
        alumno_id=alumno.id,
        filename=foto.filename or "foto.jpg",
        content_type=foto.content_type,
        fileobj=foto.file,
    )
    alumno.foto_perfil_url = url
    db.commit()
    return FotoPerfilResponse(fotoPerfilUrl=url)


@router.post("/{id}/email", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def send_email(id: int, db: Session = Depends(get_db)) -> MessageResponse:
    service = AlumnosService(db)
    alumno = service.get_alumno(id)
    message = (
        "Alumno: "
        f"{alumno.nombres} {alumno.apellidos}\n"
        f"Matricula: {alumno.matricula}\n"
        f"Promedio: {alumno.promedio}"
    )
    publish_alumno_email(message)
    return MessageResponse(message="Email enviado")


@router.post("/{id}/session/login", response_model=SessionResponse, status_code=status.HTTP_200_OK)
def session_login(
    id: int,
    body: SessionLogin,
    db: Session = Depends(get_db),
) -> SessionResponse:
    service = AlumnosService(db)
    alumno = service.get_alumno(id)
    if alumno.password != body.password:
        return _raise_invalid_session()

    session_string = secrets.token_hex(64)
    create_session_item(alumno_id=alumno.id, session_string=session_string)
    return SessionResponse(sessionString=session_string)


@router.post("/{id}/session/verify", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def session_verify(
    id: int,
    body: SessionAction,
    db: Session = Depends(get_db),
) -> MessageResponse:
    service = AlumnosService(db)
    service.get_alumno(id)
    item = find_session_item(alumno_id=id, session_string=body.sessionString)
    if not item or not item.get("active", {}).get("BOOL", False):
        return _raise_invalid_session()
    return MessageResponse(message="Sesion valida")


@router.post("/{id}/session/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def session_logout(
    id: int,
    body: SessionAction,
    db: Session = Depends(get_db),
) -> MessageResponse:
    service = AlumnosService(db)
    service.get_alumno(id)
    item = find_session_item(alumno_id=id, session_string=body.sessionString)
    if not item or not item.get("active", {}).get("BOOL", False):
        return _raise_invalid_session()
    deactivate_session_item(item)
    return MessageResponse(message="Sesion cerrada")


def _raise_invalid_session():
    from fastapi import HTTPException

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sesion invalida")
