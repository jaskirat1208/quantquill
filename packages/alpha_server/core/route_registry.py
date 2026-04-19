from fastapi import APIRouter
from typing import List, Dict, Any
import inspect

class RouteRegistry:
    """Registry for auto-discovering and managing API routes"""
    
    def __init__(self):
        self.routers: List[APIRouter] = []
    
    def register_router(self, router: APIRouter):
        """Register a router for auto-inclusion"""
        self.routers.append(router)
    
    def get_all_routers(self) -> List[APIRouter]:
        """Get all registered routers"""
        return self.routers

# Global registry instance
registry = RouteRegistry()

def register_route(prefix: str = "", tags: List[str] = None, dependencies: List[Any] = None):
    """
    Decorator to automatically register a router with the application
    
    Usage:
        @register_route(prefix="/api", tags=["api"])
        class MyRouter:
            def __init__(self):
                self.router = APIRouter(prefix=prefix, tags=tags)
                
            @self.router.get("/")
            async def root(self):
                return {"message": "Hello"}
    """
    def decorator(cls):
        # Create instance of the class, passing config for router creation
        instance = cls(prefix=prefix, tags=tags, dependencies=dependencies)
        
        # Check if the class has a router attribute
        if hasattr(instance, 'router') and isinstance(instance.router, APIRouter):
            # Auto-register the router
            registry.register_router(instance.router)
        else:
            raise ValueError(f"Class {cls.__name__} must have a 'router' attribute of type APIRouter")
        
        return cls
    
    return decorator

def auto_discover_routers(app, routers_dir: str = "routers"):
    """
    Automatically discover and include all routers in the specified directory
    
    This function will:
    1. Import all modules in the routers directory
    2. Find any classes decorated with @register_route
    3. Include their routers in the FastAPI app
    """
    import os
    import importlib
    from pathlib import Path
    
    routers_path = Path(routers_dir)
    if not routers_path.exists():
        return
    
    # Import all router modules
    for module_file in routers_path.glob("*.py"):
        if module_file.name.startswith("__"):
            continue
            
        module_name = f"{routers_dir}.{module_file.stem}"
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")
    
    # Include all registered routers
    for router in registry.get_all_routers():
        app.include_router(router)
