import logging
import sys
from pathlib import Path
from typing import Optional

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
    
