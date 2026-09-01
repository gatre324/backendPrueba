import logging

from app.modules.users.infrastructure.models import UserModel

logger = logging.getLogger(__name__)


class LoggingEmailSender:
    """Development adapter until a real SMTP provider is configured."""

    def send_confirmation(self, user: UserModel) -> None:
        logger.info("Confirmation email pending provider configuration for %s", user.email)
