"""
Базовый класс для обработки исключений app.

Включает в себя:
- Логирование ошибок.
- Формирование ответа с ошибкой.
- Генерация уникального идентификатора для ошибки.
- Преобразование даты и времени в формат ISO 8601 с учетом часового пояса.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from loguru import logger

import pytz
from fastapi import HTTPException

moscow_tz = pytz.timezone("Europe/Moscow")


class BaseAPIException(HTTPException):
    """
    Base class for handling application exceptions.

    Attributes:
        status_code: HTTP status code.
        detail: Error message.
        error_type: Type of the error.
        extra: Additional context data.

    Raises:
        HTTPException: Exception with the specified status code and message.

    Returns:
        None
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:

        self.error_type = error_type  # Save error_type
        self.extra = extra or {}  # Save extra

        context = {
            "timestamp": datetime.now(moscow_tz).isoformat(),
            "request_id": str(uuid.uuid4()),
            "status_code": status_code,
            "error_type": error_type,
            **(extra or {}),
        }

        logger.error(detail, extra=context)
        super().__init__(status_code=status_code, detail=detail)
