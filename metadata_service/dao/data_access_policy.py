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
"""Convenience methods for adding, updating, and retrieving Data Access Policy objects"""

from typing import List, Dict
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import get_collection
from metadata_service.models import DataAccessPolicy

COLLECTION_NAME = DataAccessPolicy.__collection__


async def retrieve_daps() -> List[Dict]:
    """Retrieve a list of DAPs from metadata store.

    Returns:
      A list of DAP objects.

    """
    collection = await get_collection(COLLECTION_NAME)
    daps = await collection.find().to_list(None)
    return daps


async def get_dap(dap_id: str, embedded=False) -> Dict:
    """Given a DAP ID, get the DAP object from metadata store.

    Args:
        dap_id: The DAP ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The DAP object

    """
    collection = await get_collection(COLLECTION_NAME)
    dap = await collection.find_one({"id": dap_id})
    if not dap:
        raise HTTPException(
            status_code=404,
            detail=f"{DataAccessPolicy.__name__} with id '{dap_id}' not found",
        )
    if embedded:
        dap = await embed_references(dap, DataAccessPolicy)
    return dap


async def add_dap(data: Dict) -> Dict:
    """Add a DAP object to the metadata store.

    Args:
        data: The DAP object

    Returns:
      The added DAP object

    """
    collection = await get_collection(COLLECTION_NAME)
    dap_id = data["id"]
    await collection.insert_one(data)
    dap = await get_dap(dap_id)
    return dap


async def update_dap(dap_id: str, data: Dict) -> Dict:
    """Given a DAP ID and data, update the DAP in metadata store.

    Args:
        DAP_id: The DAP ID
        data: The DAP object

    Returns:
      The updated DAP object

    """
    dap = await get_dap(dap_id)
    dap.update(**data)
    return dap
