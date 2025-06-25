from config.config_utils import Singleton
from sqlalchemy.ext.asyncio import create_async_engine 

class DBEngine(metaclass=Singleton):
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.engine = None

    def get_engine(self):
        if self.engine is None:
            connection_string = f"sqlite+aiosqlite:///./{self.db_name}"
            self.engine = create_async_engine(connection_string, echo=True, future=True)
        return self.engine