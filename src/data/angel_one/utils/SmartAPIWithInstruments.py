import SmartApi as api
import requests
from datetime import datetime, timedelta
import json
import os
import time
from av_core.logger import LoggerConfig
from data.angel_one.utils.constants import INSTRUMENTS_URL, INSTRUMENTS_CACHE_PATH, CANDLE_INFO_MAX_DAYS


class SmartConnect(api.SmartConnect):

    def __init__(self, api_key=None, access_token=None, refresh_token=None, feed_token=None, userId=None, root=None, debug=False, timeout=None, proxies=None, pool=None, disable_ssl=False, accept=None, userType=None, sourceID=None, Authorization=None, clientPublicIP=None, clientMacAddress=None, clientLocalIP=None, privateKey=None):
        super().__init__(api_key, access_token, refresh_token, feed_token, userId, root, debug, timeout, proxies, pool, disable_ssl, accept, userType, sourceID, Authorization, clientPublicIP, clientMacAddress, clientLocalIP, privateKey)
        self.logger = LoggerConfig.get_logger("SmartConnect")
        self.loadInstruments()

    def loadInstruments(self):
        """
        Loads the list of instruments and builds symbol/token lookup maps.

        Instruments are cached locally by date. If today's cache exists, it is loaded
        from disk; otherwise instruments are fetched from the API and saved to cache.
        """
        instruments_file_path = f"{INSTRUMENTS_CACHE_PATH}instruments.{datetime.now().strftime('%Y%m%d')}.json"
        instruments = []
        try:
            # Check if the instruments file for today already exists            
            if os.path.exists(instruments_file_path):
                with open(instruments_file_path, 'r') as f:
                    instruments = json.load(f)
                    self.logger.info(f"Loaded {len(instruments)} instruments from cache: {instruments_file_path}")
            
            else:  
                instruments = self._fetchInstrumentsFromAPI()
                self.logger.info(f"Fetched instruments from API. Total instruments: {len(instruments)}")
                # Save it to a file for faster access in the future
                os.makedirs(os.path.dirname(instruments_file_path), exist_ok=True)
                with open(instruments_file_path, 'w') as f:
                    json.dump(instruments, f)

                
        except Exception as e:
            self.logger.error(f"Error loading instruments: {e}")


        self.logger.info("Instruments loaded. Creating symbol and token maps for quick lookup...")        

        self.symbol_map = {}
        self.token_map = {}
        for instrument in instruments:
            if 'symbol' not in instrument or 'token' not in instrument:
                self.logger.warning(f"Instrument missing 'symbol' or 'token': {instrument}")
                continue
            self.symbol_map[instrument['symbol']] = instrument
            self.token_map[instrument['token']] = instrument

        self.logger.info(f"Symbol map and token map created with {len(self.symbol_map)} entries each.")

    def _fetchInstrumentsFromAPI(self):
        response = requests.get(INSTRUMENTS_URL)
        response.raise_for_status()
        return response.json()

    def getInstrumentBySymbol(self, symbol: str):
        """
        Fetches the instrument details for the specified symbol.

        Args:
            symbol (str): The symbol for which to fetch instrument details.

        Returns:
            dict: The instrument details for the specified symbol.
        """
        try:
            instrument = self.symbol_map.get(symbol)
            if not instrument:
                self.logger.warning(f"Instrument not found for symbol: {symbol}")
            return instrument
        except Exception as e:
            self.logger.error(f"Error fetching instrument details for symbol {symbol}: {e}")
            raise e

    def getInstrumentByToken(self, token: str):
        """
        Fetches the instrument details for the specified token.

        Args:
            token (str): The token for which to fetch instrument details.

        Returns:
            dict: The instrument details for the specified token.
        """
        try:
            instrument = self.token_map.get(token)
            if not instrument:
                self.logger.warning(f"Instrument not found for token: {token}")
            return instrument
        except Exception as e:
            self.logger.error(f"Error fetching instrument details for token {token}: {e}")
            raise e

    def _request(self, route, method, parameters=None, num_retries=3):
        now = datetime.now()
        if not hasattr(self, '_rate_limited_calls'):
            self._rate_limited_calls = {}

        # Clean up entries older than 1 minute
        self._rate_limited_calls = {k: v for k, v in self._rate_limited_calls.items() 
                                   if now.second - k <= 60}
        if now.second in self._rate_limited_calls:
            self._rate_limited_calls[now.second] += 1
        else:
            self._rate_limited_calls[now.second] = 1
        if self._rate_limited_calls[now.second] > 5:
            self.logger.warning(f"Rate limited: too many requests in one second. Retrying in 1 second.")
            time.sleep(1)
            return self._request(route, method, parameters, num_retries)
        return self._requestHelper(route, method, parameters, num_retries)

    def _requestHelper(self, route, method, parameters=None, num_retries=3):
        while(num_retries > 0 ):
            try:
                res = super()._request(route, method, parameters)
                if(res['errorcode']):
                    self.logger.error(f"Error in _request: {res['errorcode']}")
                    if(res['errorcode'] == 'AG8002'):
                        self.logger.warning("Access token expired, renewing...")
                        self.renewAccessToken()
                        self.logger.info("Access token renewed successfully. Please ensure your tokens are upto date.")
                        num_retries -= 1
                        continue

                    raise Exception(f"API Error: {res['errorcode']} - {res.get('message', '')}")
                else:
                    return res
            except Exception as e:
                self.logger.error(f"Error in _request: {e}")
                num_retries -= 1
                time.sleep(1)
                if num_retries == 0:
                    raise e

    def renewAccessToken(self):
        response =self._postRequest('api.refresh', {
            "jwtToken": self.access_token,
            "refreshToken": self.refresh_token,
            
        })
       
        tokenSet={}

        if "jwtToken" in response['data']:
            tokenSet['jwtToken']=response['data']['jwtToken']

        if "feedToken" in response['data']:
            tokenSet['feedToken']=response['data']['feedToken']

        tokenSet['clientcode']=self.userId   
        tokenSet['refreshToken']=response['data']["refreshToken"]
       
        return tokenSet

    def getCandleDataMultiDay(self, historicDataParams):
        """
        Get candle data for extended periods by splitting requests into chunks.
                
        Args:
            historicDataParams (dict): Dictionary containing:
                - exchange (str): Exchange name
                - symboltoken (str): Token symbol
                - interval (str): Time interval
                - fromdate (str): Start date in ISO format
                - todate (str): End date in ISO format
                
        Returns:
            dict: Dictionary with 'data' key containing candle data list
        """
        try:
            fromdate = datetime.fromisoformat(historicDataParams.get("fromdate"))
            todate = datetime.fromisoformat(historicDataParams.get("todate"))

            interval = historicDataParams.get("interval")
            if interval not in CANDLE_INFO_MAX_DAYS:
                raise ValueError(f"Unsupported interval: {interval}")
            max_days = CANDLE_INFO_MAX_DAYS[interval]
            if (todate - fromdate).days > max_days:
                candle_data = []
                total_days = (todate - fromdate).days + 1  # Include both start and end dates
                for i in range(0, total_days, max_days):
                    new_fromdate = fromdate + timedelta(days=i)
                    new_todate = min(fromdate + timedelta(days=i + max_days - 1), todate)
                    self.logger.info(f"Fetching candle data for {historicDataParams['symboltoken']} from {new_fromdate} to {new_todate}")
                    single_day_candle_data = super().getCandleData({
                        "exchange": historicDataParams["exchange"],
                        "symboltoken": historicDataParams["symboltoken"],
                        "interval": historicDataParams["interval"],
                        "fromdate": new_fromdate.strftime('%Y-%m-%d %H:%M'),
                        "todate": new_todate.strftime('%Y-%m-%d %H:%M')
                    })
                    candle_data += single_day_candle_data['data']
                
                self.logger.info(f"Total candle data fetched for {historicDataParams['symboltoken']}: {len(candle_data)}")
                
                return {'data': candle_data}
            

            
            candle_data = super().getCandleData(historicDataParams)
            return candle_data
        except Exception as e:
            self.logger.error(f"Error fetching candle data: {e}")
            raise e


if __name__ == "__main__":
    app = SmartConnect()
    pass
