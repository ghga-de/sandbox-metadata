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

COLLECTION_NAME = "studies"


async def retrieve_studies():
    collection = get_collection(COLLECTION_NAME)
    studies = await collection.distinct('id')
    return studies


async def get_study(study_id):
    collection = get_collection(COLLECTION_NAME)
    study = await collection.find_one({'id': study_id})
    if not study:
        raise HTTPException(status_code=404, detail=f"Study with id '{study_id}' not found")
    return study


async def add_study(data: Dict):
    collection = get_collection(COLLECTION_NAME)
    study_id = data['id']
    r = await collection.insert_one(data)
    study = await get_study(study_id)
    return study


async def update_study(study_id: str, data: Dict):
    study = await get_study(study_id)
    study.update(**data)
    return study
