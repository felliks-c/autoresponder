# app/main.py
from fastapi import FastAPI
from app.api.routers import auth, messages, sessions
from app.core.logging import setup_logging

def get_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Async NLP Microservice", version="0.1.0")
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(messages.router, prefix="/message", tags=["messages"])
    app.include_router(sessions.router, prefix="/session", tags=["sessions"])
    return app

app = get_app()
