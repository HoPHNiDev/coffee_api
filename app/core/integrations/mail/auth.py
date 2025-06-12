from pydantic import EmailStr

from core.exceptions import EmailSendError
from core.integrations.mail.base import MailBaseService


class MailAuthService(MailBaseService):
    """
    Сервис для отправки писем, связанных с аутентификацией.
    """

    @staticmethod
    async def send_verification_message(
        recipients: list[EmailStr], template_body: dict[str, str]
    ):
        """
        Sending a verification email to the user.

        Args:
            recipients (list[EmailStr]): list of emails of recipients.
            template_body (dict[str, str] | None): Email template data

        Returns:
            None
        """
        message = MailAuthService.create_message(
            subject="Подтверждение регистрации",
            recipients=recipients,
            template_body=template_body,
        )
        try:
            await MailAuthService.send_email(
                message=message, template_name="verification.html"
            )
        except Exception as e:
            raise EmailSendError() from e
