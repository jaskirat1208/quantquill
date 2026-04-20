

from fastapi import APIRouter, Query
from models.etc.instruments import get_instruments
from core.route_registry import register_route
from typing import Optional, List

@register_route(prefix="/instruments", tags=["instruments"])
class InstrumentsRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes
        self.router.add_api_route("/all", self.get_all_instruments, methods=["GET"])
        self.router.add_api_route("/search", self.search_instruments, methods=["GET"])

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

    async def search_instruments(
        self,
        search: Optional[str] = Query(None, description="Search term to filter instruments"),
        exchange: Optional[str] = Query(None, description="Filter by exchange"),
        instrument_type: Optional[str] = Query(None, description="Filter by instrument type"),
        page: int = Query(1, ge=1, description="Page number (1-based)"),
        page_size: int = Query(50, ge=1, le=1000, description="Number of items per page")
    ):
        """
        Search and filter instruments with pagination.

        Args:
            search: Search term that matches symbol, name, or other text fields
            exchange: Filter by specific exchange (NSE, BSE, etc.)
            instrument_type: Filter by instrument type (EQ, FUT, OPT, etc.)
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Filtered and paginated instruments with pagination metadata
        """
        instruments = get_instruments()

        # Apply filters
        filtered_instruments = instruments

        if search:
            search_lower = search.lower()
            filtered_instruments = [
                instrument for instrument in filtered_instruments
                if self._matches_search(instrument, search_lower)
            ]

        if exchange:
            exchange_upper = exchange.upper()
            filtered_instruments = [
                instrument for instrument in filtered_instruments
                if instrument.get('exch_seg', '').upper() == exchange_upper
            ]

        if instrument_type:
            instrument_type_upper = instrument_type.upper()
            filtered_instruments = [
                instrument for instrument in filtered_instruments
                if instrument.get('instrumenttype', '').upper() == instrument_type_upper
            ]

        # Sort results by symbol for consistent ordering
        filtered_instruments.sort(key=lambda x: x.get('symbol', ''))

        total_items = len(filtered_instruments)

        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        # Get paginated data
        paginated_instruments = filtered_instruments[start_idx:end_idx]

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
            },
            "filters": {
                "search": search,
                "exchange": exchange,
                "instrument_type": instrument_type
            }
        }

    def _matches_search(self, instrument: dict, search_term: str) -> bool:
        """
        Check if an instrument matches the search term.

        Args:
            instrument: Instrument dictionary
            search_term: Lowercase search term

        Returns:
            True if instrument matches search criteria
        """
        # Search in multiple fields
        searchable_fields = [
            'symbol',
            'name',
            'tradingsymbol',
            'series',
            'instrumenttype',
            'exch_seg',
            'tick_size',
            'lotsize'
        ]

        for field in searchable_fields:
            field_value = instrument.get(field, '')
            if field_value and isinstance(field_value, str):
                if search_term in field_value.lower():
                    return True

        # Also search in numeric fields converted to string
        numeric_fields = ['token', 'strike']
        for field in numeric_fields:
            field_value = instrument.get(field)
            if field_value is not None:
                if search_term in str(field_value):
                    return True

        return False
