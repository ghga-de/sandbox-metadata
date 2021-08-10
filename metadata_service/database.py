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
from metadata_service.config import get_config

CLIENT = None


async def get_db():
    """Return database client instance."""
    config = get_config()
    global CLIENT
    if not CLIENT:
        CLIENT = motor.motor_asyncio.AsyncIOMotorClient(config.db_url)
    return CLIENT


async def close_db():
    """Close database connection."""
    global CLIENT
    CLIENT.close()


async def get_collection(name):
    """Get a collection"""
    config = get_config()
    client = await get_db()
    collection = client[config.db_name].get_collection(name)
    return collection
