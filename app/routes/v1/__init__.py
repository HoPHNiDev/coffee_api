from routes.base import BaseRouter
from routes.v1.auth import AuthRouter
from routes.v1.user import UserRouter

class APIv1(BaseRouter):
    def configure_routes(self):
        self.router.include_router(AuthRouter().get_router())
        self.router.include_router(UserRouter().get_router())
