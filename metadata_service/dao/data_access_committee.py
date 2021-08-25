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

"""Convenience methods for adding, updating, and retrieving Data Access Committee objects"""

from typing import List
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import DBConnect
from metadata_service.models import DataAccessCommittee

COLLECTION_NAME = DataAccessCommittee.__collection__
PREFIX = "DAC:"


async def retrieve_dacs() -> List[DataAccessCommittee]:
    """Retrieve a list of DACs from metadata store.

    Returns:
      A list of DAC objects.

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    dacs = await collection.find().to_list(None)  # type: ignore
    await db_connect.close_db()
    return dacs


async def get_dac(dac_id: str, embedded=False) -> DataAccessCommittee:
    """Given a DAC ID, get the DAC object from metadata store.

    Args:
        dac_id: The DAC ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The DAC object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    dac = await collection.find_one({"id": dac_id})  # type: ignore
    if not dac:
        raise HTTPException(
            status_code=404,
            detail=f"{DataAccessCommittee.__name__} with id '{dac_id}' not found",
        )
    if embedded:
        dac = await embed_references(dac, DataAccessCommittee)
    await db_connect.close_db()
    return dac


async def add_dac(data: DataAccessCommittee) -> DataAccessCommittee:
    """Add a DAC object to the metadata store.

    Args:
        data: The DAC object

    Returns:
      The added DAC object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    dac_id = await db_connect.get_next_id(COLLECTION_NAME, PREFIX)
    data.id = dac_id
    await collection.insert_one(data.dict())  # type: ignore
    await db_connect.close_db()
    dac = await get_dac(dac_id)
    return dac


async def update_dac(dac_id: str, data: DataAccessCommittee) -> DataAccessCommittee:
    """Given a DAC ID and data, update the DAC in metadata store.

    Args:
        dac_id: The DAC ID
        data: The DAC object

    Returns:
      The updated DAC object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    await collection.update_one(  # type: ignore
        {"id": dac_id}, {"$set": data.dict(exclude_unset=True)}
    )
    await db_connect.close_db()
    dac = await get_dac(dac_id)
    return dac
