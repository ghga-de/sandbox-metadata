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
from fastapi import APIRouter

from metadata_service.dao.data_access_committee import (
    get_dac,
    add_dac,
    update_dac,
    retrieve_dacs,
)
from metadata_service.models import DataAccessCommittee


data_access_committee_router = APIRouter()


@data_access_committee_router.get("/data_access_committees", response_model=List[str])
async def get_all_dacs():
    dacs = await retrieve_dacs()
    return dacs


@data_access_committee_router.get("/data_access_committees/{dac_id}", response_model=DataAccessCommittee)
async def get_dacs(dac_id, embedded: bool = False):
    dac = await get_dac(dac_id, embedded)
    return dac


@data_access_committee_router.post("/data_access_committees", response_model=DataAccessCommittee)
async def add_dacs(data: Dict):
    dac = await add_dac(data)
    return dac


@data_access_committee_router.put("/data_access_committees/{dac_id}", response_model=DataAccessCommittee)
async def update_dacs(dac_id, data: Dict):
    dac = await update_dac(dac_id, data)
    return dac
