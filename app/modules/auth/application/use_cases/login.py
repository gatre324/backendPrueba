from app.core.exceptions import InactiveUserError, InvalidCredentialsError
from app.core.security.jwt import create_access_token
from app.core.security.passwords import verify_password
from app.modules.auth.application.schemas import AuthResponse, LoginRequest
from app.modules.users.infrastructure.repositories import SqlAlchemyUserRepository


class LoginUserUseCase:
    def __init__(self, users: SqlAlchemyUserRepository) -> None:
        self.users = users

    def execute(self, request: LoginRequest) -> AuthResponse:
        user = self.users.get_by_email(str(request.email).lower())
        if user is None or not verify_password(request.password, user.password_hash):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError()
        token = create_access_token(subject=str(user.id), user_type=user.user_type)
        return AuthResponse(access_token=token, user=user)
