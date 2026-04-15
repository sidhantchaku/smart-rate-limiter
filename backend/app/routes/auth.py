from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.schemas import LoginRequest, TokenResponse, UserProfile
from app.services.auth import authenticate_user, create_access_token, decode_token

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = authenticate_user(payload.username, payload.password)
    token, expires_in = create_access_token(
        {"sub": user["username"], "plan": user["plan"]}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in,
    }


@router.get("/me", response_model=UserProfile)
def me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(credentials.credentials)
    return {
        "username": payload["sub"],
        "plan": payload["plan"],
    }
