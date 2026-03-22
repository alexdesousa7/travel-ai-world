from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRoleUpdate
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_users(self, skip: int = 0, limit: int = 100):
        return await self.repository.get_all(skip=skip, limit=limit)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Return the User if credentials are valid, otherwise None."""
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_in: UserCreate) -> User:
        db_obj = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
            role=user_in.role
        )
        return await self.repository.create(db_obj)

    async def update_user(self, db_obj: User, user_in: UserUpdate | UserRoleUpdate) -> User:
        """
        Update a user from a Pydantic model or dict.
        Supports partial updates dynamically.
        """
        if hasattr(user_in, "model_dump"):
            update_data = user_in.model_dump(exclude_unset=True)
        elif isinstance(user_in, dict):
            update_data = user_in
        else:
            update_data = {}

        for field, value in update_data.items():
            if field == "password" and value is not None:
                setattr(db_obj, "hashed_password", get_password_hash(value))
            elif hasattr(db_obj, field):
                setattr(db_obj, field, value)

        return await self.repository.update(db_obj)

    async def delete_user(self, db_obj: User) -> None:
        await self.repository.delete(db_obj)
