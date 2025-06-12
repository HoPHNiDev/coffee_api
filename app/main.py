import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routes.v1 import APIv1


def create_application() -> FastAPI:
    """
    Create and configure FastAPI app
    """
    app = FastAPI(**settings.app_params)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    v1_router = APIv1()
    v1_router.configure_routes()
    app.include_router(v1_router.get_router(), prefix="/api/v1")

    return app


app = create_application()

if __name__ == "__main__":
    uvicorn.run("main:app", **settings.uvicorn_params)
