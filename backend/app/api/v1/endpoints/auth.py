import logging

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_user_service
from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token, verify_google_token
from app.schemas.user import GoogleAuthRequest
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    """
    OAuth2-compatible login endpoint.

    Accepts username (email) + password via form data and returns a Bearer token.
    The Swagger UI "Authorize" button uses this endpoint automatically.
    """
    user = await user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise UnauthorizedException(detail="Incorrect email or password")
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user account")

    return {
        "access_token": create_access_token(subject=user.id),
        "token_type": "bearer",
    }


@router.post("/google")
async def google_auth(
    body: GoogleAuthRequest,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """Verify Google ID token from frontend, find/create user, return JWT.

    Frontend sends the credential from GoogleLogin widget.
    Backend validates it with Google, creates/updates user in DB,
    and returns our own JWT for subsequent API calls.
    """
    try:
        google_data = await verify_google_token(body.credential)
    except ValueError as exc:
        raise UnauthorizedException(detail=str(exc))

    user = await user_service.find_or_create_google_user(
        email=google_data["email"],
        google_id=google_data["sub"],
        name=google_data.get("name", ""),
        picture=google_data.get("picture"),
    )

    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user account")

    return {
        "access_token": create_access_token(subject=user.id),
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
        },
    }
