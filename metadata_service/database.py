# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    This module contains the DBConnect class and related methods
"""
import motor.motor_asyncio
from metadata_service.config import get_config

COUNTER = "counter"


class DBConnect:
    """
    class Database
    """

    def __init__(self) -> None:
        config = get_config()
        self.db_url = config.db_url
        self.db_name = config.db_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient()

    async def get_db(self):
        """
        Return database client instance.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.db_url)
        return self.client

    async def close_db(self):
        """
        Close database connection.
        """
        self.client.close()

    async def get_collection(self, name) -> object:
        """
        Get a collection
        """
        client = await self.get_db()
        collection = client[self.db_name][name]
        return collection

    async def get_next_id(self, collection_name, prefix):
        """
        This method generates the sequence id for the MongoDB document
        """
        collection = await self.get_collection(COUNTER)
        document = await collection.find_one({"_id": collection_name})  # type: ignore
        collection.update_one({"_id": collection_name}, {"$inc": {"value": 1}})  # type: ignore
        await self.close_db()
        return prefix + f"{(document['value'] + 1):07}"
