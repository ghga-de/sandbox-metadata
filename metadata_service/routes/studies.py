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

from metadata_service.models import Study
from metadata_service.routes import DB_NAME, MONGODB_URL

STUDY_COLLECTION = "studies"

studies_router = APIRouter()


@studies_router.get("/studies", response_model=List[str])
async def get_all_studies():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    studies = await collection.distinct('id')
    return studies


@studies_router.get("/studies/{study_id}", response_model=Study)
async def get_studies(study_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    study = await collection.find_one({'id': study_id})
    if not study:
        raise HTTPException(status_code=404, detail=f"Study with id '{study_id}' not found")
    return study


@studies_router.put("/studies/{study_id}", response_model=Study)
async def update_studies(study_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    study = await collection.find_one({'id': study_id})
    if not study:
        raise HTTPException(status_code=404, detail=f"Study with id '{study_id}' not found")
    study.update(**data)
    return study

