

from fastapi import APIRouter, Query
from models.etc.instruments import get_instruments
from core.route_registry import register_route

@register_route(prefix="/instruments", tags=["instruments"])
class InstrumentsRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)
        
        # Register routes
        self.router.add_api_route("/all", self.get_all_instruments, methods=["GET"])
    
    async def get_all_instruments(
        self,
        page: int = Query(1, ge=1, description="Page number (1-based)"),
        page_size: int = Query(100, ge=1, le=1000, description="Number of items per page")
    ):
        instruments = get_instruments()
        total_items = len(instruments)
        
        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get paginated data
        paginated_instruments = instruments[start_idx:end_idx]
        
        # Calculate pagination metadata
        total_pages = (total_items + page_size - 1) // page_size
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            "instruments": paginated_instruments,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev
            }
        }

