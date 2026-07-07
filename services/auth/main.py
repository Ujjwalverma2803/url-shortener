from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Handles user registration, login and JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "auth"
    }