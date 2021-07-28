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

from typing import Dict
from fastapi.exceptions import HTTPException
from metadata_service.database import get_collection

COLLECTION_NAME = "publication"


async def retrieve_publications():
    collection = await get_collection(COLLECTION_NAME)
    publications = await collection.distinct("id")
    return publications


async def get_publication(publication_id):
    collection = await get_collection(COLLECTION_NAME)
    publication = await collection.find_one({"id": publication_id})
    if not publication:
        raise HTTPException(
            status_code=404, detail=f"Publication with id '{publication_id}' not found"
        )
    return publication


async def add_publication(data: Dict):
    collection = await get_collection(COLLECTION_NAME)
    publication_id = data["id"]
    await collection.insert_one(data)
    publication = await get_publication(publication_id)
    return publication


async def update_publication(publication_id: str, data: Dict):
    publication = await get_publication(publication_id)
    publication.update(**data)
    return publication
