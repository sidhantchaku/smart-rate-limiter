from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import api, auth

app = FastAPI(
    title="Smart API Rate Limiter",
    description="JWT-protected API with Redis-backed rate limiting.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(api.router, tags=["api"])


@app.get("/")
def root():
    return {
        "message": "Smart API Rate Limiter is running",
        "docs": "/docs",
    }
