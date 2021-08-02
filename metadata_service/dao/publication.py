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

from typing import List, Dict
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import get_collection
from metadata_service.models import Publication

COLLECTION_NAME = Publication.__collection__


async def retrieve_publications() -> List[str]:
    """Retrieve a list of Publications from metadata store.

    Returns:
      A list of Publication IDs.

    """
    collection = await get_collection(COLLECTION_NAME)
    publications = await collection.distinct("id")
    return publications


async def get_publication(publication_id: str, embedded: bool = False) -> Dict:
    """Given a Publication ID, get the Publication object from metadata store.

    Args:
        publication_id: The Publication ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The Publication object

    """
    collection = await get_collection(COLLECTION_NAME)
    publication = await collection.find_one({"id": publication_id})
    if not publication:
        raise HTTPException(
            status_code=404, detail=f"{Publication.__name__} with id '{publication_id}' not found"
        )
    if embedded:
        publication = await embed_references(publication, Publication)
    return publication


async def add_publication(data: Dict) -> Dict:
    """Add a Publication object to the metadata store.

    Args:
        data: The Publication object

    Returns:
      The added Publication object

    """
    collection = await get_collection(COLLECTION_NAME)
    publication_id = data["id"]
    await collection.insert_one(data)
    publication = await get_publication(publication_id)
    return publication


async def update_publication(publication_id: str, data: Dict) -> Dict:
    """Given a Publication ID and data, update the Publication in metadata store.

    Args:
        publication_id: The Publication ID
        data: The Publication object

    Returns:
      The updated Publication object

    """
    publication = await get_publication(publication_id)
    publication.update(**data)
    return publication
