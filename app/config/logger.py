from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL 
from config.config_utils import Singleton
import sys

class Logger(metaclass=Singleton):
    """
    A simple logger class that provides methods to log messages at different levels.
    """
    
    def __init__(self, name: str, level: int = DEBUG):
        self.logger = getLogger(name)
        self.logger.setLevel(level)

        handler = StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

