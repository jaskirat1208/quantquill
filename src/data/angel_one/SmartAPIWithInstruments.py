import SmartApi as api
import requests
from datetime import datetime
import json
import os

from av_core.logger import LoggerConfig
from data.angel_one.constants import INSTRUMENTS_URL, INSTRUMENTS_CACHE_PATH

class SmartConnect(api.SmartConnect):

    def __init__(self, api_key=None, access_token=None, refresh_token=None, feed_token=None, userId=None, root=None, debug=False, timeout=None, proxies=None, pool=None, disable_ssl=False, accept=None, userType=None, sourceID=None, Authorization=None, clientPublicIP=None, clientMacAddress=None, clientLocalIP=None, privateKey=None):
        super().__init__(api_key, access_token, refresh_token, feed_token, userId, root, debug, timeout, proxies, pool, disable_ssl, accept, userType, sourceID, Authorization, clientPublicIP, clientMacAddress, clientLocalIP, privateKey)
        self.logger = LoggerConfig.get_logger("SmartConnect")
        self.loadInstruments()

    def loadInstruments(self):
        """
        Loads the list of instruments for the specified exchange and stores it in the instance variable.

        Args:
            exchange (str): The name of the exchange for which to load instruments.
        """
        instruments_file_path = f"{INSTRUMENTS_CACHE_PATH}instruments.{datetime.now().strftime('%Y%m%d')}.json"
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
        instruments_json = requests.get(INSTRUMENTS_URL)
        return instruments_json.json()

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

if __name__ == "__main__":
    app = SmartConnect()
    app.loadInstruments()
    pass