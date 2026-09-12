from fastapi import APIRouter, Query
from typing import Optional
from alpha_server.core.route_registry import register_route
from alpha_server.models.etc import instruments as instapi
from quantquill.data.angel_one.utils.app import AngelOneSmartApp
import pandas as pd

@register_route(prefix="/oi_monitor", tags=["oi_monitor"])
class OIMonitorRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes
        self.router.add_api_route("/", self.get_oi_data, methods=["GET"])
    
    async def get_oi_data(self, 
        underlying: str = Query(..., description="Underlying symbol"),
        strike: int = Query(..., description="Strike price(INR)"),
        expiry: str = Query(..., description="Expiry date (DDMMMYY)"),
        interval: str = Query(..., description="Interval: (ONE_MINUTE|THREE_MINUTE|FIVE_MINUTE)")
    ):
        if not underlying: 
            return []
        
        # TODO: Implement OI data retrieval logic
        call_name = f"{underlying}{expiry}{strike}CE"
        put_name = f"{underlying}{expiry}{strike}PE"
        platform = AngelOneSmartApp(instance_name='oi_monitor')
        client = platform.get_client()
        oi_data = []
        for sym in [call_name, put_name]:
            tok = client.getInstrumentBySymbol(sym)
            resp = client.getOIData({
                "exchange": tok['exch_seg'], 
                "symboltoken": tok['token'],
                "interval": interval,
                "fromdate": "2026-09-11 09:11",
                "todate": "2026-09-11 15:00"
            })
            oi_data.append(resp['data'])

        call_oi = oi_data[0]
        put_oi = oi_data[1]
        
        # Create DataFrames from the data
        call_df = pd.DataFrame(call_oi)
        put_df = pd.DataFrame(put_oi)
        
        # Rename OI columns to distinguish call vs put
        call_df = call_df.rename(columns={'oi': 'call_oi', 'time': 'timestamp'})
        put_df = put_df.rename(columns={'oi': 'put_oi', 'time': 'timestamp'})
        
        # Merge on timestamp to get full time series
        merged_df = pd.merge(call_df[['timestamp', 'call_oi']], 
                            put_df[['timestamp', 'put_oi']], 
                            on='timestamp', 
                            how='outer')
        
        # Sort by timestamp
        merged_df = merged_df.sort_values('timestamp')
        
        # Calculate OI change (current - previous)
        merged_df['call_oi_change'] = merged_df['call_oi'].diff()
        merged_df['put_oi_change'] = merged_df['put_oi'].diff()
        
        # Replace NaN values with 0
        merged_df = merged_df.fillna(0)
        
        return merged_df.to_dict(orient='records')


        
