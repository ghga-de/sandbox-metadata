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

from metadata_service.dao.publication import get_publication, retrieve_publications, add_publication, update_publication
from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadata_service.models import Publication


publication_router = APIRouter()


@publication_router.get("/publications", response_model=List[str])
async def get_all_publications():
    publications = await retrieve_publications()
    return publications


@publication_router.get("/publications/{publication_id}", response_model=Publication)
async def get_publications(publication_id):
    publication = await get_publication(publication_id)
    return publication


@publication_router.put("/publications/{publication_id}", response_model=Publication)
async def update_publications(publication_id, data: dict):
    publication = await update_publication(publication_id, data)
    return publication

