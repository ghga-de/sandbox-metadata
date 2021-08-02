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


@data_access_committee_router.get("/data_access_committees", response_model=List[str], summary="Get all DAC IDs")
async def get_all_dacs():
    """Retrieve a list of DAC IDs from metadata store."""
    dacs = await retrieve_dacs()
    return dacs


@data_access_committee_router.get("/data_access_committees/{data_access_committee_id}", response_model=DataAccessCommittee, summary="Get a DAC")
async def get_dacs(data_access_committee_id: str, embedded: bool = False):
    """Given a DAC ID, get the DAC from metadata store."""
    dac = await get_dac(data_access_committee_id, embedded)
    return dac


@data_access_committee_router.post("/data_access_committees", response_model=DataAccessCommittee, summary="Add a DAC")
async def add_dacs(data: Dict):
    """Add a DAC to the metadata store."""
    dac = await add_dac(data)
    return dac


@data_access_committee_router.put("/data_access_committees/{data_access_committee_id}", response_model=DataAccessCommittee, summary="Update a DAC")
async def update_dacs(data_access_committee_id: str, data: Dict):
    """Given a DAC ID and data, update the DAC in metadata store."""
    dac = await update_dac(data_access_committee_id, data)
    return dac
