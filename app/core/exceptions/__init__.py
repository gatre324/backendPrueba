class AppError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class DuplicateEmailError(AppError):
    def __init__(self) -> None:
        super().__init__("EMAIL_ALREADY_REGISTERED", "El correo ya está registrado")


class InvalidCredentialsError(AppError):
    def __init__(self) -> None:
        super().__init__("INVALID_CREDENTIALS", "Correo o contraseña incorrectos")


class InactiveUserError(AppError):
    def __init__(self) -> None:
        super().__init__("USER_INACTIVE", "La cuenta está deshabilitada")


class InvalidTokenError(AppError):
    def __init__(self) -> None:
        super().__init__("INVALID_TOKEN", "El token no es válido o ha expirado")
