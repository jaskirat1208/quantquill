from fastapi import APIRouter, Query
from typing import Optional, List
from alpha_server.core.route_registry import register_route
from alpha_server.models.etc import instruments as instapi
from quantquill.data.angel_one.utils.app import AngelOneSmartApp
import pandas as pd
from datetime import datetime
from quantquill.data.angel_one.utils.SmartAPIWithInstruments import SmartConnect
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

# Singleton instance of AngelOneSmartApp
_platform_instance = None

def get_platform():
    """Get or create the singleton AngelOneSmartApp instance."""
    global _platform_instance
    if _platform_instance is None:
        _platform_instance = AngelOneSmartApp(instance_name='oi_monitor')
    return _platform_instance

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
        platform = get_platform()
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
        start_time = time.time()
        logger.info(f"[PROFILE] get_multiple_strikes_oi START - underlying={underlying}, strikes={strikes}, expiry={expiry}, interval={interval}, date={date}")
        
        platform = get_platform()
        client = platform.get_client()
        logger.info(f"[PROFILE] Platform client obtained in {time.time() - start_time:.3f}s")
        
        # Create tasks for concurrent execution
        tasks = []
        for strike in strikes:
            option_template = f"{underlying}{expiry}{strike}"
            # Run blocking get_oi_data in thread pool
            task = asyncio.to_thread(self.get_oi_data, option_template, interval, date, client)
            tasks.append(task)
        
        logger.info(f"[PROFILE] Created {len(tasks)} tasks in {time.time() - start_time:.3f}s")
        
        # Execute all requests concurrently
        gather_start = time.time()
        oi_data_list = await asyncio.gather(*tasks)
        logger.info(f"[PROFILE] asyncio.gather completed in {time.time() - gather_start:.3f}s")
        
        concat_start = time.time()
        oi_data_agg_df = pd.concat(oi_data_list).groupby("timestamp").sum().reset_index()
        logger.info(f"[PROFILE] concat + groupby completed in {time.time() - concat_start:.3f}s")
        
        result = self.calculate_pcr(oi_data_agg_df)
        logger.info(f"[PROFILE] calculate_pcr completed in {time.time() - concat_start:.3f}s")
        logger.info(f"[PROFILE] get_multiple_strikes_oi TOTAL: {time.time() - start_time:.3f}s")
        
        return result


    def get_oi_data(self, option_template: str,  interval: str, date: str, smartapi_client: SmartConnect):
        start_time = time.time()
        logger.info(f"[PROFILE] get_oi_data START - option_template={option_template}")
        
        call_name = f"{option_template}CE"
        put_name = f"{option_template}PE"
        oi_data = []
        
        for sym in [call_name, put_name]:
            sym_start = time.time()
            tok = smartapi_client.getInstrumentBySymbol(sym)
            logger.info(f"[PROFILE] getInstrumentBySymbol({sym}) completed in {time.time() - sym_start:.3f}s")
            
            api_start = time.time()
            resp = smartapi_client.getOIData({
                "exchange": tok['exch_seg'], 
                "symboltoken": tok['token'],
                "interval": interval,
                "fromdate": f"{date} 00:00",
                "todate": f"{date} 23:59"
            })
            logger.info(f"[PROFILE] getOIData({sym}) completed in {time.time() - api_start:.3f}s")
            oi_data.append(resp['data'])
        
        logger.info(f"[PROFILE] get_oi_data TOTAL for {option_template}: {time.time() - start_time:.3f}s")

        call_oi = oi_data[0]
        put_oi = oi_data[1]
        
        # Create DataFrames from the data
        df_start = time.time()
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
        logger.info(f"[PROFILE] DataFrame operations completed in {time.time() - df_start:.3f}s")
        
        return merged_df

    def calculate_pcr(self, oi_data_df):
        # Calculate OI change (current - previous)
        oi_data_df['call_oi_change'] = oi_data_df['call_oi'].diff()
        oi_data_df['put_oi_change'] = oi_data_df['put_oi'].diff()
        oi_data_df['put_call_ratio'] = oi_data_df['put_oi'] / oi_data_df['call_oi']
        oi_data_df['put_call_ratio_change'] = oi_data_df['put_call_ratio'].diff()
        oi_data_df['put_call_difference'] = oi_data_df['put_oi'] - oi_data_df['call_oi']
        oi_data_df['put_call_diff_change'] = oi_data_df['put_call_difference'].diff()
        
        # Replace NaN values with 0
        oi_data_df = oi_data_df.fillna(0)
        
        return oi_data_df.to_dict(orient='records')