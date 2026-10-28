from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interfaces.user_interface import UserInterface
from app.models.user import User


class UserRepository(UserInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch user by unique email address, returning User or None."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Fetch user by primary key id, returning User or None."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        """Add a user instance to the session and flush to generate its ID."""
        self.session.add(user)
        await self.session.flush()
        return user
