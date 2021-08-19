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

"""Routes for Publication objects"""

from typing import List, Dict
from fastapi import APIRouter

from metadata_service.dao.publication import (
    get_publication,
    retrieve_publications,
    add_publication,
    update_publication,
)
from metadata_service.models import Publication


publication_router = APIRouter()


@publication_router.get(
    "/publications", response_model=List[Publication], summary="Get all Publications"
)
async def get_all_publications():
    """Retrieve a list of Publication IDs from metadata store."""
    publications = await retrieve_publications()
    return publications


@publication_router.get(
    "/publications/{publication_id}",
    response_model=Publication,
    summary="Get a Publication",
)
async def get_publications(publication_id: str, embedded: bool = False):
    """Given a Publication ID, get the Publication from metadata store."""
    publication = await get_publication(publication_id, embedded)
    return publication


@publication_router.post(
    "/publications", response_model=Publication, summary="Add a Publication"
)
async def add_publications(data: Dict):
    """Add a Publication to the metadata store."""
    publication = await add_publication(data)
    return publication


@publication_router.put(
    "/publications/{publication_id}",
    response_model=Publication,
    summary="Update a Publication",
)
async def update_publications(publication_id: str, data: dict):
    """Given a Publication ID and data, update the Publication in metadata store."""
    publication = await update_publication(publication_id, data)
    return publication
