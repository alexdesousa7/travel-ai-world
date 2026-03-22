from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2-compatible login endpoint.

    Accepts username (email) + password via form data and returns a Bearer token.
    The Swagger UI "Authorize" button uses this endpoint automatically.
    """
    user_service = UserService(db)
    user = await user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise UnauthorizedException(detail="Incorrect email or password")
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user account")

    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
