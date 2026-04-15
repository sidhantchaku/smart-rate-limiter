from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.schemas import RateLimitStatus
from app.services.auth import decode_token
from app.services.rate_limiter import SmartRateLimiter

router = APIRouter()
security = HTTPBearer()
rate_limiter = SmartRateLimiter(limit=5, window_seconds=60)


def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    return decode_token(credentials.credentials)


def client_key(request: Request, user: dict) -> str:
    ip = request.client.host if request.client else "unknown"
    return f"{user['sub']}:{ip}"


@router.get("/protected-api")
def protected_api(request: Request, user: dict = Depends(current_user)):
    status_payload = rate_limiter.check(client_key(request, user))
    if not status_payload["allowed"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "Rate limit exceeded",
                "limit": status_payload["limit"],
                "remaining": status_payload["remaining"],
                "reset_in_seconds": status_payload["reset_in_seconds"],
            },
        )

    return {
        "message": f"Hello {user['sub']}, your request was accepted.",
        "plan": user["plan"],
        "rate_limit": {
            "limit": status_payload["limit"],
            "remaining": status_payload["remaining"],
            "reset_in_seconds": status_payload["reset_in_seconds"],
            "source": status_payload["source"],
        },
    }


@router.get("/rate-limit/status", response_model=RateLimitStatus)
def rate_limit_status(request: Request, user: dict = Depends(current_user)):
    status_payload = rate_limiter.check(client_key(request, user))
    return {
        "limit": status_payload["limit"],
        "remaining": status_payload["remaining"],
        "reset_in_seconds": status_payload["reset_in_seconds"],
        "source": status_payload["source"],
    }
