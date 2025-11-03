from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import Config

class DataBase:

    MODELS: list
    
    async def init(self):
        mongodb_client = AsyncIOMotorClient(Config.MONGODB_DATABASE_URI)
        database = mongodb_client.get_database(Config.DATABASE_NAME)
        
        await init_beanie(
            database=database,
            document_models=self.MODELS
        )