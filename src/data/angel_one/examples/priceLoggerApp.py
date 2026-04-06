from typing import Optional

from data.angel_one.app import AngelOneSmartApp


class PriceLoggerApp(AngelOneSmartApp):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        super().__init__(config_file=config_file, log_file=log_file, instance_name=instance_name)

    def start(self):
        self.logger.info("PriceLoggerApp started.")
        # Add logic to subscribe to price updates and log them

if(__name__ == "__main__"):
    app = PriceLoggerApp()
    app.start()
