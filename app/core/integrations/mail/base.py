from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr
from loguru import logger
from core.config import settings

mail_config = ConnectionConfig(**settings.mail_params)
mail = FastMail(mail_config)


class MailBaseService:

    @staticmethod
    def create_message(
        subject: str,
        recipients: list[EmailStr],
        body: str | None = None,
        template_body: dict[str, str] | None = None,
        subtype: MessageType = MessageType.html,
    ) -> MessageSchema:
        return MessageSchema(
            subject=subject,
            body=body,
            recipients=recipients,
            template_body=template_body,
            subtype=subtype,
        )

    @staticmethod
    async def send_email(
        message: MessageSchema,
        template_name: str | None = None,
    ) -> None:
        try:
            await mail.send_message(message=message, template_name=template_name)
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            logger.exception(e)
            raise e
