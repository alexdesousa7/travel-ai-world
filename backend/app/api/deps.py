from fastapi import Depends
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services.user_service import UserService

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise UnauthorizedException(detail="Invalid authentication credentials")
    except (jwt.InvalidTokenError, ValidationError):
        raise UnauthorizedException(detail="Invalid or expired token")

    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id=int(token_data))
    if not user:
        # 401, not 404: avoids leaking which user IDs exist in the database
        raise UnauthorizedException(detail="Invalid authentication credentials")
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user account")
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise UnauthorizedException(detail="The user doesn't have enough privileges")
    return current_user


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Provides a UserService instance via FastAPI dependency injection.

    Centralises service construction so tests can override it with a mock
    by using app.dependency_overrides[get_user_service].
    """
    return UserService(db)
