from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.router import api_router
from app.db import Base, engine
from app.exceptions import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AWS Alumnos", version="1.0.0")
register_exception_handlers(app)
app.include_router(api_router)
