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

import motor.motor_asyncio

DB_URL = "mongodb://localhost:27017"
DB_NAME = "metadata"

client = None


async def get_db():
    """Return database client instance."""
    global client
    if not client:
        client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
    return client


async def close_db():
    """Close database connection."""
    global client
    client.close()


async def get_collection(name):
    """Get a collection"""
    global client
    collection = client.metadata.get_collection(name)
    return collection
