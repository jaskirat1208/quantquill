import logging
import sys
from pathlib import Path
from typing import Optional
from av_core.cred_reader import CredentialsReader

class LoggerConfig:
    """Configure and provide logging across the application."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def setup(
        cls,
        name: str = "app",
        level: int = logging.INFO,
        log_file: Optional[str] = None
    ) -> logging.Logger:
        """Initialize and configure logger."""
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)
        
        return cls._logger
    
    @classmethod
    def get_logger(cls, name: str = "app") -> logging.Logger:
        """Get or create logger instance."""
        if cls._logger is None:
            cls.setup(name=name)
        return cls._logger
    

class App:
    """Main application class to initialize components."""
    
    def __init__(self, config_file: Optional[str] = None,  log_file: Optional[str] = None, instance_name: str = ""):
        if(not config_file):
            config_file = f"./configs/{__name__}{'.' + instance_name if instance_name else ''}.cnf"
        self.logger = LoggerConfig.setup(log_file=log_file)
        self.config = CredentialsReader(config_file).getConfig() if config_file else None
        self.logger.info("Application initialized successfully.")
        
# Example usage
if __name__ == "__main__":
    logger = LoggerConfig.get_logger()
    logger.info("Logger initialized successfully.")