from av_core.logger import LoggerConfig
from typing import Optional
from av_core.cred_reader import CredentialsReader


class App:
    """Main application class to initialize components."""
    
    def __init__(self, config_file: Optional[str] = None,  log_file: Optional[str] = None, instance_name: str = ""):
        if(not config_file):
            config_file = f"./configs/{__name__}{'.' + instance_name if instance_name else ''}.cnf"
        self.logger = LoggerConfig.setup(log_file=log_file)

        cred_reader = CredentialsReader(config_file)
        self.config = cred_reader.getConfig()
        self.logger.info("Application initialized successfully.")
        
# Example usage
if __name__ == "__main__":
    logger = LoggerConfig.get_logger()
    logger.info("Logger initialized successfully.")