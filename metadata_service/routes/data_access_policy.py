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

from metadata_service.dao.data_access_policy import (
    get_dap,
    add_dap,
    update_dap,
    retrieve_daps,
)
from metadata_service.models import DataAccessPolicy


data_access_policy_router = APIRouter()


@data_access_policy_router.get("/data_access_policies", response_model=List[str])
async def get_all_daps():
    daps = await retrieve_daps()
    return daps


@data_access_policy_router.get("/data_access_policies/{dap_id}", response_model=DataAccessPolicy)
async def get_daps(dap_id, embedded: bool = False):
    dap = await get_dap(dap_id, embedded)
    return dap


@data_access_policy_router.post("/data_access_policies", response_model=DataAccessPolicy)
async def add_daps(data: Dict):
    dap = await add_dap(data)
    return dap


@data_access_policy_router.put("/data_access_policies/{dap_id}", response_model=DataAccessPolicy)
async def update_daps(dap_id, data: Dict):
    dap = await update_dap(dap_id, data)
    return dap
