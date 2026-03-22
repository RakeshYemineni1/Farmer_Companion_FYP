from motor.motor_asyncio import AsyncIOMotorClient
from backend.core.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.krishisaathi
    # Ensure unique indexes
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True)


async def close_db():
    global client
    if client:
        client.close()


def get_db():
    return db
