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

from metadata_service.core.utils import embed_references
from metadata_service.database import get_collection
from metadata_service.models import DataAccessCommittee

COLLECTION_NAME = DataAccessCommittee.__collection__


async def retrieve_dacs():
    collection = await get_collection(COLLECTION_NAME)
    dacs = await collection.distinct("id")
    return dacs


async def get_dac(dac_id, embedded = False):
    collection = await get_collection(COLLECTION_NAME)
    dac = await collection.find_one({"id": dac_id})
    if not dac:
        raise HTTPException(
            status_code=404, detail=f"{DataAccessCommittee.__name__} with id '{dac_id}' not found"
        )
    if embedded:
        dac = await embed_references(dac, DataAccessCommittee)
    return dac


async def add_dac(data: Dict):
    collection = await get_collection(COLLECTION_NAME)
    dac_id = data["id"]
    await collection.insert_one(data)
    dac = await get_dac(dac_id)
    return dac


async def update_dac(dac_id: str, data: Dict):
    dac = await get_dac(dac_id)
    dac.update(**data)
    return dac
