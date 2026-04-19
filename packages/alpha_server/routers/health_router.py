from fastapi import APIRouter
from core.route_registry import register_route

@register_route(tags=["health"])
class HealthRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes
        self.router.add_api_route("/", self.root, methods=["GET"])
        self.router.add_api_route("/health", self.health_check, methods=["GET"])
    
    async def root(self):
        return {"message": "Alpha Server - QuantQuill API", "status": "running"}

    async def health_check(self):
        return {"status": "healthy", "service": "alpha-server"}
