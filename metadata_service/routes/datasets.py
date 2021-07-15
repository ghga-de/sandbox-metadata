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

from metadata_service.dao.dataset import get_dataset, add_dataset, update_dataset, retrieve_datasets
from typing import List, Dict

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadata_service.models import Dataset


dataset_router = APIRouter()


@dataset_router.get("/datasets", response_model=List[str])
async def get_all_datasets():
    datasets = await retrieve_datasets()
    return datasets


@dataset_router.get("/datasets/{dataset_id}", response_model=Dataset)
async def get_datasets(dataset_id):
    dataset = await get_dataset(dataset_id)


@dataset_router.put("/datasets/{dataset_id}", response_model=Dataset)
async def update_datasets(dataset_id, data: Dict):
    dataset = await update_dataset(dataset_id, data)
    return dataset
