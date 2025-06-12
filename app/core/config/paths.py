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


    BASE_DIR = find_project_root()

    APP_DIR = BASE_DIR / "app"
    ENV_FILE = APP_DIR / ".env"
