from loguru import logger

from core.utils.singleton import Singleton

class LoggingSettings(Singleton):
    LOG_FILE: str = "./logs/app.log"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}"
    LEVEL: str = "DEBUG"
    ROTATION: int = 10485760  # 10MB
    RETENTION: str = "1 week"
    BACKUP_COUNT: int = 5

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        logger.add(
            sink=self.LOG_FILE,
            format=self.LOG_FORMAT,
            level=self.LEVEL,
            rotation=self.ROTATION,
            retention=self.RETENTION,
            enqueue=True,
        )

