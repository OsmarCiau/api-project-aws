from fastapi import FastAPI

from app.api.router import api_router
from app.exceptions import register_exception_handlers

app = FastAPI(title="AWS Alumnos", version="1.0.0")
register_exception_handlers(app)
app.include_router(api_router)
