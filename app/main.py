import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings


def create_application() -> FastAPI:
    """
    Создает и настраивает экземпляр приложения FastAPI.
    """
    app = FastAPI(**settings.app_params)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", **settings.uvicorn_params)
