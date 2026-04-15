from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.routes import api, auth

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Smart API Rate Limiter",
    description="JWT-protected API with Redis-backed rate limiting and a built-in frontend.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(api.router, prefix="/api", tags=["api"])


@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")
