from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import strategy executor (relative imports for running from alpha_server directory)
from core.route_registry import registry
import sys
print(f"Python path: {sys.path}")
print(f"Working dir: {__import__('os').getcwd()}")

# Import routers to trigger auto-registration
import routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize your quantquill library
    print("Alpha Server started - QuantQuill library initialized")
    yield
    # Shutdown: Cleanup resources
    print("Alpha Server shutting down")

app = FastAPI(
    title="Alpha Server",
    description="QuantQuill Strategy Execution API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all registered routers from the registry
print("Including registered routers...")
for router in registry.get_all_routers():
    app.include_router(router)
    print(f"  Included router: {router.prefix if router.prefix else '/'}")

# Print all registered routes for debugging
print("All registered routes:")
for route in app.routes:
    if hasattr(route, 'methods'):
        print(f"  {list(route.methods)} {route.path}")
    else:
        print(f"  {route.path}")

# Fallback root endpoint
@app.get("/")
async def root():
    return {"message": "Alpha Server - QuantQuill API", "status": "running", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8091,
        reload=True
    )
