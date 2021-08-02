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
from metadata_service.models import Dataset

COLLECTION_NAME = Dataset.__collection__


async def retrieve_datasets() -> List[str]:
    """Retrieve a list of Datasets from metadata store.

    Returns:
      A list of Dataset IDs.

    """
    collection = await get_collection(COLLECTION_NAME)
    datasets = await collection.distinct("id")
    return datasets


async def get_dataset(dataset_id: str, embedded = False) -> Dict:
    """Given a Datset ID, get the Dataset object from metadata store.

    Args:
        dataset_id: The Dataset ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
      The Dataset object

    """
    collection = await get_collection(COLLECTION_NAME)
    dataset = await collection.find_one({"id": dataset_id})
    if not dataset:
        raise HTTPException(
            status_code=404, detail=f"{Dataset.__name__} with id '{dataset_id}' not found"
        )
    if embedded:
        dataset = await embed_references(dataset, Dataset)
    return dataset


async def add_dataset(data: Dict) -> Dict:
    """Add a Dataset object to the metadata store.

    Args:
        data: The Dataset object

    Returns:
      The added Dataset object

    """
    collection = await get_collection(COLLECTION_NAME)
    dataset_id = data["id"]
    await collection.insert_one(data)
    dataset = await get_dataset(dataset_id)
    return dataset


async def update_dataset(dataset_id: str, data: Dict) -> Dict:
    """Given a Dataset ID and data, update the Dataset in metadata store.

    Args:
        dataset_id: The Dataset ID
        data: The Dataset object

    Returns:
      The updated Dataset object

    """
    dataset = await get_dataset(dataset_id)
    dataset.update(**data)
    return dataset
