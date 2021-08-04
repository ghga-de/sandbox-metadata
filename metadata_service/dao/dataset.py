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

from typing import Dict
from fastapi.exceptions import HTTPException
from metadata_service.database import get_collection

COLLECTION_NAME = "dataset"


async def retrieve_datasets():
    collection = await get_collection(COLLECTION_NAME)
    datasets = await collection.distinct("id")
    return datasets


async def get_dataset(dataset_id):
    collection = await get_collection(COLLECTION_NAME)
    dataset = await collection.find_one({"id": dataset_id})
    if not dataset:
        raise HTTPException(
            status_code=404, detail=f"Dataset with id '{dataset_id}' not found"
        )
    return dataset


async def add_dataset(data: Dict):
    collection = await get_collection(COLLECTION_NAME)
    dataset_id = data["id"]
    await collection.insert_one(data)
    dataset = await get_dataset(dataset_id)
    return dataset


async def update_dataset(dataset_id: str, data: Dict):
    collection = await get_collection(COLLECTION_NAME)
    await collection.update_one({"id": dataset_id}, {"$set": data})
    dataset = await get_dataset(dataset_id)
    return dataset
