from typing import Optional, Sequence

from fastapi import APIRouter


class BaseRouter:
    """
    Base class for all routes.

    Provides general functionality for creating regular and secure routes.

    Attributes:
        router (APIRouter): Base FastAPI Router
    """

    def __init__(self, prefix: str = "", tags: Optional[Sequence[str]] = None):
        """
        Initialize base router.

        Args:
            prefix (str): URL prefixes for all routes
            tags (List[str]): Tags list for Swagger docs
        """
        self.router = APIRouter(prefix=f"/{prefix}" if prefix else "", tags=tags or [])
        self.configure()

    def configure(self):
        """Redefined in child classes for configuring routes"""
        pass

    def get_router(self) -> APIRouter:
        """Returns the configured FastAPI router.

        Returns:
            APIRouter: Configured FastAPI Router"""
        return self.router
