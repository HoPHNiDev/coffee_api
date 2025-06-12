from pathlib import Path
from loguru import logger


class PathSettings:
    @staticmethod
    def find_project_root() -> Path:
        """Finding the project root directory based on marker files."""
        current_dir = Path.cwd()

        markers = [".git", "pyproject.toml", "README.md"]

        for parent in [current_dir, *current_dir.parents]:
            if any((parent / marker).exists() for marker in markers):
                return parent

        logger.warning(
            "Could not determine the project root, using the current directory"
        )
        return current_dir

    @staticmethod
    def check_and_create_directory(path: Path) -> None:
        """Check if the directory exists, if not, create it."""
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
        else:
            logger.info(f"Directory already exists: {path}")


    BASE_DIR = find_project_root()
    ENV_FILE = BASE_DIR / ".env"

    APP_DIR = BASE_DIR / "app"
    CORE_DIR = APP_DIR / "core"

    TEMPLATES_DIR = CORE_DIR / "templates"
    EMAIL_TEMPLATES_DIR = TEMPLATES_DIR / "mail"

    KEY_DIR = CORE_DIR / "keys"
    check_and_create_directory(KEY_DIR)

    PUBLIC_KEY_PATH = KEY_DIR / "jwt-public.pem"
    PRIVATE_KEY_PATH = KEY_DIR / "jwt-private.pem"
