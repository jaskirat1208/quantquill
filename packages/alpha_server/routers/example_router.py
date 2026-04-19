from fastapi import APIRouter
from core.route_registry import register_route

@register_route(prefix="/example", tags=["example"])
class ExampleRouter:
    """Example router to demonstrate auto-discovery"""

    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes - these will be auto-discovered!
        self.router.add_api_route("/test", self.root, methods=["GET"])
        self.router.add_api_route("/hello/{name}", self.say_hello, methods=["GET"])
    
    async def root(self):
        return {"message": "This is an example router - auto-discovered!"}
    
    async def say_hello(self, name: str):
        return {"message": f"Hello, {name}!"}

    # The /api prefix is added by FastAPI's router middleware. If you're
    # using FastAPI's built-in server, you'll need to include the /api
    # prefix in your URL. If you're using a different server or middleware,
    # you may need to adjust the URL accordingly.
