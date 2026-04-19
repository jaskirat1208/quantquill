from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import strategy executor
from models.models import StrategyExecutor
from core.route_registry import auto_discover_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize your quantquill library
    app.state.strategy_executor = StrategyExecutor()
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

# Auto-discover and include all routers
auto_discover_routers(app, "routers")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8091,
        reload=True
    )
