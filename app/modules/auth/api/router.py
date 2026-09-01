from fastapi import APIRouter, HTTPException, Response, status

from app.core.dependencies.auth import CurrentUser
from app.core.dependencies.database import DbSession
from app.core.exceptions import AppError
from app.modules.auth.application.schemas import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)
from app.modules.auth.application.use_cases.login import LoginUserUseCase
from app.modules.auth.application.use_cases.register import RegisterUserUseCase
from app.modules.auth.infrastructure.email import LoggingEmailSender
from app.modules.users.infrastructure.repositories import SqlAlchemyUserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


def app_error(exc: AppError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT if exc.code == "EMAIL_ALREADY_REGISTERED" else status.HTTP_401_UNAUTHORIZED,
        detail={"code": exc.code, "message": exc.message},
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: DbSession) -> RegisterResponse:
    try:
        user = RegisterUserUseCase(SqlAlchemyUserRepository(db), LoggingEmailSender()).execute(request)
    except AppError as exc:
        raise app_error(exc) from exc
    return RegisterResponse(message="Cuenta creada correctamente", user=user)


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: DbSession) -> AuthResponse:
    try:
        return LoginUserUseCase(SqlAlchemyUserRepository(db)).execute(request)
    except AppError as exc:
        raise app_error(exc) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_: CurrentUser) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser) -> UserResponse:
    return current_user
