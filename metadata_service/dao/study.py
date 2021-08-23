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

"""Convenience methods for adding, updating, and retrieving Study objects"""

from typing import List, Dict
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import DBConnect
from metadata_service.models import Study

COLLECTION_NAME = Study.__collection__
PREFIX = "STU:"


async def retrieve_studies() -> List[Dict]:
    """Retrieve a list of Studies from metadata store.

    Returns:
      A list of Study objects.

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    studies = await collection.find().to_list(None)  # type: ignore
    db_connect.close_db()
    return studies


async def get_study(study_id: str, embedded: bool = False) -> Dict:
    """Given a Study ID, get the Study object from metadata store.

    Args:
        study_id: The Study ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The Study object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    study = await collection.find_one({"id": study_id})  # type: ignore
    if not study:
        raise HTTPException(
            status_code=404, detail=f"{Study.__name__} with id '{study_id}' not found"
        )
    if embedded:
        study = await embed_references(study, Study)
    db_connect.close_db()
    return study


async def add_study(data: Dict) -> Dict:
    """Add a Study object to the metadata store.

    Args:
        data: The Study object

    Returns:
      The added Study object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    study_id = await db_connect.get_next_id(COLLECTION_NAME, PREFIX)
    await collection.insert_one(data)  # type: ignore
    study = await get_study(study_id)
    db_connect.close_db()
    return study


async def update_study(study_id: str, data: Dict) -> Dict:
    """Given a Study ID and data, update the Study in metadata store.

    Args:
        study_id: The Study ID
        data: The Study object

    Returns:
      The updated Study object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    await collection.update_one({"id": study_id}, {"$set": data})  # type: ignore
    study = await get_study(study_id)
    db_connect.close_db()
    return study
