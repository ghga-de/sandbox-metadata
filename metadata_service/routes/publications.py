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

from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadata_service.models import Publication
from metadata_service.routes import DB_NAME, MONGODB_URL

PUBLICATION_COLLECTION = "publications"

publication_router = APIRouter()


@publication_router.get("/publications", response_model=List[str])
async def get_all_publications():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publications = await collection.distinct('id')
    return publications


@publication_router.get("/publications/{publication_id}", response_model=Publication)
async def get_publications(publication_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publication = await collection.find_one({'id': publication_id})
    if not publication:
        raise HTTPException(status_code=404, detail=f"Publication with id '{publication_id}' not found")
    return publication


@publication_router.put("/publications/{publication_id}", response_model=Publication)
async def update_publications(publication_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publication = await collection.find_one({'id': publication_id})
    if not publication:
        raise HTTPException(status_code=404, detail=f"Publication with id '{publication_id}' not found")
    publication.update(**data)
    return publication

