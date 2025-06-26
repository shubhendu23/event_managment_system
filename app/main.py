from config.logger import Logger
from config.db_config import DBEngine

db = DBEngine(db_name="../data/event_management.sqlite").get_engine()
logger = Logger(name="EventManagementAPI", level=10).logger

from api.routes import app
import uvicorn

if __name__ == "__main__":
    
    logger.info("Starting Event Management API server")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
    logger.info("Event Management API server started")
