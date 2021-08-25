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

from typing import List
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import DBConnect
from metadata_service.models import DataAccessPolicy

COLLECTION_NAME = DataAccessPolicy.__collection__
PREFIX = "DAP:"


async def retrieve_daps() -> List[DataAccessPolicy]:
    """Retrieve a list of DAPs from metadata store.

    Returns:
      A list of DAP objects.

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    daps = await collection.find().to_list(None)  # type: ignore
    await db_connect.close_db()
    return daps


async def get_dap(dap_id: str, embedded=False) -> DataAccessPolicy:
    """Given a DAP ID, get the DAP object from metadata store.

    Args:
        dap_id: The DAP ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The DAP object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    dap = await collection.find_one({"id": dap_id})  # type: ignore
    if not dap:
        raise HTTPException(
            status_code=404,
            detail=f"{DataAccessPolicy.__name__} with id '{dap_id}' not found",
        )
    if embedded:
        dap = await embed_references(dap, DataAccessPolicy)
    await db_connect.close_db()
    return dap


async def add_dap(data: DataAccessPolicy) -> DataAccessPolicy:
    """Add a DAP object to the metadata store.

    Args:
        data: The DAP object

    Returns:
      The added DAP object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    dap_id = await db_connect.get_next_id(COLLECTION_NAME, PREFIX)
    data.id = dap_id
    await collection.insert_one(data.dict())  # type: ignore
    await db_connect.close_db()
    dap = await get_dap(dap_id)
    return dap


async def update_dap(dap_id: str, data: DataAccessPolicy) -> DataAccessPolicy:
    """Given a dap ID and data, update the dap in metadata store.

    Args:
        dap_id: The DAP ID
        data: The DAP object

    Returns:
      The updated DAP object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    await collection.update_one(  # type: ignore
        {"id": dap_id}, {"$set": data.dict(exclude_unset=True)}
    )
    await db_connect.close_db()
    dap = await get_dap(dap_id)
    return dap
