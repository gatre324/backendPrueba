from typing import Protocol

from app.modules.users.infrastructure.models import UserModel


class EmailSender(Protocol):
    def send_confirmation(self, user: UserModel) -> None: ...
