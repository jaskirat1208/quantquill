from fastapi import APIRouter, Query
from typing import Optional, List
from alpha_server.core.route_registry import register_route
from alpha_server.models.etc import instruments as instapi
from quantquill.data.angel_one.utils.app import AngelOneSmartApp
import pandas as pd
from datetime import datetime

@register_route(prefix="/oi_monitor", tags=["oi_monitor"])
class OIMonitorRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes
        self.router.add_api_route("/", self.get_single_strike_oi, methods=["GET"])
        self.router.add_api_route("/multi", self.get_multiple_strikes_oi, methods=["GET"])
    
    async def get_single_strike_oi(self, 
        underlying: str = Query(..., description="Underlying symbol"),
        strike: int = Query(..., description="Strike price(INR)"),
        expiry: str = Query(..., description="Expiry date (DDMMMYY)"),
        interval: str = Query(..., description="Interval: (ONE_MINUTE|THREE_MINUTE|FIVE_MINUTE)"),
        date: str = Query(..., description="Date (YYYY-MM-DD)")
    ):
        platform = AngelOneSmartApp(instance_name='oi_monitor')
        client = platform.get_client()
        option_template = f"{underlying}{expiry}{strike}"
        oi_data_df = self.get_oi_data(option_template, interval, date, client)
        return self.calculate_pcr(oi_data_df)
        

    async def get_multiple_strikes_oi(self,
            underlying: str = Query(..., description="Underlying symbol"),
            strikes: List[int] = Query(default=[], description="Strike price(INR) - repeat parameter for multiple values"),
            expiry: str = Query(..., description="Expiry date (DDMMMYY)"),
            interval: str = Query(..., description="Interval: (ONE_MINUTE|THREE_MINUTE|FIVE_MINUTE)"),
            date: str = Query(..., description="Date (YYYY-MM-DD)")
    ):
        platform = AngelOneSmartApp(instance_name='oi_monitor')
        client = platform.get_client()
        oi_data_list = []
        for strike in strikes:
            option_template = f"{underlying}{expiry}{strike}"
            oi_data = self.get_oi_data(option_template, interval, date, client)
            oi_data_list.append(oi_data)
        
        oi_data_agg_df = pd.concat(oi_data_list).groupby("timestamp").sum().reset_index()
        return self.calculate_pcr(oi_data_agg_df)


    def get_oi_data(self, option_template: str,  interval: str, date: str, smartapi_client):
        call_name = f"{option_template}CE"
        put_name = f"{option_template}PE"
        oi_data = []
        for sym in [call_name, put_name]:
            tok = smartapi_client.getInstrumentBySymbol(sym)
            resp = smartapi_client.getOIData({
                "exchange": tok['exch_seg'], 
                "symboltoken": tok['token'],
                "interval": interval,
                "fromdate": f"{date} 00:00",
                "todate": f"{date} 23:59"
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
        
        return merged_df

    def calculate_pcr(self, oi_data_df):
        # Calculate OI change (current - previous)
        oi_data_df['call_oi_change'] = oi_data_df['call_oi'].diff()
        oi_data_df['put_oi_change'] = oi_data_df['put_oi'].diff()
        oi_data_df['put_call_ratio'] = oi_data_df['put_oi'] / oi_data_df['call_oi']
        oi_data_df['put_call_difference'] = oi_data_df['put_oi'] - oi_data_df['call_oi']
        oi_data_df['put_call_diff_change'] = oi_data_df['put_call_difference'].diff()
        
        # Replace NaN values with 0
        oi_data_df = oi_data_df.fillna(0)
        
        return oi_data_df.to_dict(orient='records')