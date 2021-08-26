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
This module contains the DBConnect class and its related methods
that are relevant for connecting to an underlying MongoDB store.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from metadata_service.config import get_config

COUNTER = "counter"


class DBConnect:
    """
    Class that handles connections to a MongoDB store.
    """

    def __init__(self):
        config = get_config()
        self.db_url = config.db_url
        self.db_name = config.db_name
        self.client = AsyncIOMotorClient()

    async def get_db(self) -> AsyncIOMotorClient:
        """
        Return database client instance.
        """
        self.client = AsyncIOMotorClient(self.db_url)
        return self.client

    async def close_db(self) -> None:
        """
        Close database connection.
        """
        self.client.close()

    async def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """
        Get a collection from the database.

        Args:
            collection_name: Name of the collection to fetch

        Returns:
            An instance of AsyncIOMotorCollection

        """
        client = await self.get_db()
        collection = client[self.db_name][collection_name]
        return collection

    async def get_next_id(self, collection_name: str, prefix: str) -> str:
        """
        This method generates the ID for a new document.
        The format of the ID depends on the ``collection_name``
        and ``prefix``.

        Args:
            collection_name: Name of the collection
            prefix: The prefix corresponding to documents of the collection

        Returns:
            The generated ID

        """
        collection = await self.get_collection(COUNTER)
        document = await collection.find_one({"_id": collection_name})  # type: ignore
        collection.update_one({"_id": collection_name}, {"$inc": {"value": 1}})  # type: ignore
        await self.close_db()
        return f"{prefix}:{(document['value'] + 1):07}"
