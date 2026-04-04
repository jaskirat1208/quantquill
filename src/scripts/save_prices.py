from strats import BaseStrat
from typing import Optional

class PriceSaverStrat(BaseStrat.BaseStrategy):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        super().__init__(config_file=config_file, log_file=log_file, instance_name=instance_name)
        self.logger.info("PriceSaverStrat initialized successfully.")

    def start(self):
        self.logger.info("PriceSaverStrat started.")
        # Initialize any necessary resources or subscriptions here

if(__name__ == "__main__"):
    strat = PriceSaverStrat()
    strat.start()