import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from bson import ObjectId

logger = logging.getLogger("realty-service")

def parse_id(id_str: str):
    """Convert string ID to ObjectId if it is a valid 24-character hex, else return string."""
    try:
        return ObjectId(id_str)
    except Exception:
        return id_str

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_db():
    """Establish connection to MongoDB cluster."""
    logger.info("Connecting to MongoDB...")
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db_instance.db = db_instance.client[settings.DB_NAME]
    logger.info("Connected to MongoDB successfully!")

async def close_db():
    """Close MongoDB connection."""
    if db_instance.client:
        logger.info("Closing MongoDB connection...")
        db_instance.client.close()
        logger.info("Closed MongoDB connection.")

def get_db():
    """Dependency injection helper to get database instance."""
    return db_instance.db
