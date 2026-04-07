from typing import Optional
import time

from data.angel_one.app import AngelOneSmartApp


class PriceLoggerApp(AngelOneSmartApp):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        super().__init__(config_file=config_file, log_file=log_file, instance_name=instance_name)

    def generate_token_on_expiry(self):
        token_data = self.m_client.renewAccessToken()
        self.m_jwt_tok = token_data['jwtToken']
        self.m_refreshToken = token_data['refreshToken']

    def start(self):
        self.logger.info("PriceLoggerApp started.")
        self.generate_token_on_expiry()
        candle_info_params = {
            "exchange": "NSE",
            "symboltoken": "99926000",
            "interval": "ONE_MINUTE",
            "fromdate": "2023-09-06 11:15",
            "todate": "2023-09-06 12:00"
        }
        while True:
            # Add logic to subscribe to price updates and log them
            response = self.m_client.getCandleData(candle_info_params)
            self.logger.info(f"Candle data: {response}")
            time.sleep(10)

if(__name__ == "__main__"):
    app = PriceLoggerApp()
    app.start()
