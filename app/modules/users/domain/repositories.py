from typing import Protocol
from uuid import UUID

from app.modules.users.infrastructure.models import UserModel


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> UserModel | None: ...

    def get_by_id(self, user_id: UUID) -> UserModel | None: ...

    def create(self, **values: object) -> UserModel: ...
