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
from metadata_service.models import File

COLLECTION_NAME = File.__collection__


async def retrieve_files() -> List[str]:
    """Retrieve a list of File IDs from metadata store.

    Returns:
      A list of File IDs.

    """
    collection = await get_collection(COLLECTION_NAME)
    files = await collection.distinct("id")
    return files


async def get_file(file_id: str, embedded: bool = False) -> Dict:
    """Given a File ID, get the File object from metadata store.

    Args:
        file_id: The File ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The File object

    """
    collection = await get_collection(COLLECTION_NAME)
    file = await collection.find_one({"id": file_id})
    if not file:
        raise HTTPException(
            status_code=404, detail=f"{File.__name__} with id '{file_id}' not found"
        )
    if embedded:
        file = await embed_references(file, File)
    return file


async def add_file(data: Dict) -> Dict:
    """Add a File object to the metadata store.

    Args:
        data: The File object

    Returns:
      The added File object

    """
    collection = await get_collection(COLLECTION_NAME)
    file_id = data["id"]
    await collection.insert_one(data)
    file = await get_file(file_id)
    return file


async def update_file(file_id: str, data: Dict) -> Dict:
    """Given a File ID and data, update the File in metadata store.

    Args:
        file_id: The File ID
        data: The File object

    Returns:
      The updated File object

    """
    file = await get_file(file_id)
    file.update(**data)
    return file
