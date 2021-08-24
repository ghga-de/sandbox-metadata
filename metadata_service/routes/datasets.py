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
"""Routes for Dataset objects"""

from typing import List
from fastapi import APIRouter

from metadata_service.dao.dataset import (
    get_dataset,
    add_dataset,
    update_dataset,
    retrieve_datasets,
)
from metadata_service.models import Dataset


dataset_router = APIRouter()


@dataset_router.get(
    "/datasets", response_model=List[Dataset], summary="Get all Datasets"
)
async def get_all_datasets():
    """Retrieve a list of Dataset IDs from metadata store."""
    datasets = await retrieve_datasets()
    return datasets


@dataset_router.get(
    "/datasets/{dataset_id}", response_model=Dataset, summary="Get a Dataset"
)
async def get_datasets(dataset_id: str, embedded: bool = False):
    """Given a Dataset ID, get the Dataset from metadata store."""
    dataset = await get_dataset(dataset_id, embedded)
    return dataset


@dataset_router.post("/datasets", response_model=Dataset, summary="Add a Dataset")
async def add_datasets(data: Dataset):
    """Add a Dataset to the metadata store."""
    dataset = await add_dataset(data)
    return dataset


@dataset_router.put(
    "/datasets/{dataset_id}", response_model=Dataset, summary="Update a Dataset"
)
async def update_datasets(dataset_id, data: Dataset):
    """Given a Dataset ID and data, update the Dataset in metadata store."""
    dataset = await update_dataset(dataset_id, data)
    return dataset
