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

"""
Routes for interacting with Data Access Policy records
"""

from typing import List
from fastapi import APIRouter

from metadata_service.dao.data_access_policy import (
    get_dap,
    add_dap,
    update_dap,
    retrieve_daps,
)
from metadata_service.models import DataAccessPolicy


data_access_policy_router = APIRouter()


@data_access_policy_router.get(
    "/data_access_policies",
    response_model=List[DataAccessPolicy],
    summary="Get all DAPs",
)
async def get_all_daps():
    """
    Retrieve a list of DAP records from the metadata store.
    """
    daps = await retrieve_daps()
    return daps


@data_access_policy_router.get(
    "/data_access_policies/{data_access_policy_id}",
    response_model=DataAccessPolicy,
    summary="Get a DAP",
)
async def get_daps(data_access_policy_id: str, embedded: bool = False):
    """
    Given a DAP ID, get the DAP record from the metadata store.
    """
    dap = await get_dap(data_access_policy_id, embedded)
    return dap


@data_access_policy_router.post(
    "/data_access_policies", response_model=DataAccessPolicy, summary="Add a DAP"
)
async def add_daps(data: DataAccessPolicy):
    """
    Add a DAP record to the metadata store.
    """
    dap = await add_dap(data)
    return dap


@data_access_policy_router.put(
    "/data_access_policies/{data_access_policy_id}",
    response_model=DataAccessPolicy,
    summary="Update a DAP",
)
async def update_daps(data_access_policy_id: str, data: DataAccessPolicy):
    """
    Given a DAP ID and data, update the DAP record in metadata store.
    """
    dap = await update_dap(data_access_policy_id, data)
    return dap
