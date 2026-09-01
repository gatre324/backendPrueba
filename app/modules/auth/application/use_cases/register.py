from app.core.exceptions import DuplicateEmailError
from app.core.security.passwords import hash_password
from app.modules.auth.application.email import EmailSender
from app.modules.auth.application.schemas import RegisterRequest
from app.modules.users.domain.enums import UserType
from app.modules.users.infrastructure.repositories import SqlAlchemyUserRepository


class RegisterUserUseCase:
    def __init__(self, users: SqlAlchemyUserRepository, email_sender: EmailSender) -> None:
        self.users = users
        self.email_sender = email_sender

    def execute(self, request: RegisterRequest):
        email = str(request.email).lower()
        if self.users.get_by_email(email) is not None:
            raise DuplicateEmailError()

        user = self.users.create(
            email=email,
            password_hash=hash_password(request.password),
            first_name=request.first_name.strip(),
            last_name=request.last_name.strip(),
            user_type=UserType.PATIENT.value,
            is_active=True,
            is_verified=False,
        )
        self.email_sender.send_confirmation(user)
        return user
