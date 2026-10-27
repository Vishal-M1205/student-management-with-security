from abc import ABC, abstractmethod
from typing import Optional
from app.models.user import User


class UserInterface(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

