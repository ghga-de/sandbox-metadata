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
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import get_collection
from metadata_service.models import Study

COLLECTION_NAME = Study.__collection__


async def retrieve_studies() -> List[str]:
    """Retrieve a list of Studies from metadata store.

    Returns:
      A list of Study IDs.

    """
    collection = await get_collection(COLLECTION_NAME)
    studies = await collection.distinct("id")
    return studies


async def get_study(study_id: str, embedded: bool = False) -> Dict:
    """Given a Study ID, get the Study object from metadata store.

    Args:
        study_id: The Study ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The Study object

    """
    collection = await get_collection(COLLECTION_NAME)
    study = await collection.find_one({"id": study_id})
    if not study:
        raise HTTPException(
            status_code=404, detail=f"{Study.__name__} with id '{study_id}' not found"
        )
    if embedded:
        study = await embed_references(study, Study)
    return study


async def add_study(data: Dict) -> Dict:
    """Add a Study object to the metadata store.

    Args:
        data: The Study object

    Returns:
      The added Study object

    """
    collection = await get_collection(COLLECTION_NAME)
    study_id = data["id"]
    await collection.insert_one(data)
    study = await get_study(study_id)
    return study


async def update_study(study_id: str, data: Dict) -> Dict:
    """Given a Study ID and data, update the Study in metadata store.

    Args:
        study_id: The Study ID
        data: The Study object

    Returns:
      The updated Study object

    """
    study = await get_study(study_id)
    study.update(**data)
    return study
