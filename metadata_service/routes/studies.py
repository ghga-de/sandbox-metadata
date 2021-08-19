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

"""Routes for Study objects"""

from typing import List, Dict
from fastapi import APIRouter

from metadata_service.dao.study import (
    add_study,
    get_study,
    retrieve_studies,
    update_study,
)
from metadata_service.models import Study


studies_router = APIRouter()


@studies_router.get("/studies", response_model=List[Study], summary="Get all Studies")
async def get_all_studies():
    """Retrieve a list of Study IDs from metadata store."""
    studies = await retrieve_studies()
    return studies


@studies_router.get("/studies/{study_id}", response_model=Study, summary="Get a Study")
async def get_studies(study_id: str, embedded: bool = False):
    """Given a Study ID, get the DAP from metadata store."""
    study = await get_study(study_id, embedded)
    return study


@studies_router.post("/studies", response_model=Study, summary="Add a Study")
async def add_studies(data: Dict):
    """Add a Study to the metadata store."""
    study = await add_study(data)
    return study


@studies_router.put(
    "/studies/{study_id}", response_model=Study, summary="Update a Study"
)
async def update_studies(study_id, data: dict):
    """Given a Study ID and data, update the Study in metadata store."""
    study = await update_study(study_id, data)
    return study
