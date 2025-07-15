from bson.objectid import ObjectId
from typing import Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient


class MongoRepository:
    """Repository for MongoDB using Motor"""

    def __init__(self, client: AsyncIOMotorClient, db: AsyncIOMotorDatabase):
        self.client = client
        self.db = db
        # self.collection = db[collection_name]

    async def create(self, data: dict, collection) -> Any:
        result = await self.db[collection].insert_one(data)
        return {**data, "_id": str(result.inserted_id)}

    async def get_by_id(self, data: Any, collection) -> Optional[Any]:
        result = await self.db[collection].find_one(data)
        return result if result else None

    async def get_by_field(self, field: str, value: Any, collection):
        return await self.db[collection].get_by_field(field, value)

    async def get_by_email(self, email: str, collection) -> Optional[Any]:
        result = await self.db[collection].find_one({"email": email})
        return result if result else None

    async def get_all(self, collection) -> List[Any]:
        return await self.db[collection].find().to_list(None)

    async def update(self, id: Any, data: dict, collection) -> Any:
        result = await self.db[collection].find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data}, return_document=True
        )
        return result

    async def delete(self, data: Any, collection) -> Any:
        result = await self.db[collection].delete_one(data)
        return result.deleted_count > 0
