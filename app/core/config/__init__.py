from .config import BASE_DIR, Settings, PathSettings

settings = Settings(env_file=PathSettings.ENV_FILE)

__all__ = [
    "BASE_DIR",
    "settings",
]
