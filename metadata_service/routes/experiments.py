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

from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadata_service.models import Experiment
from metadata_service.routes import DB_NAME, MONGODB_URL

EXPERIMENT_COLLECTION = "experiments"

experiment_router = APIRouter()


@experiment_router.get("/experiments", response_model=List[str])
async def get_all_experiments():
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[DB_NAME][EXPERIMENT_COLLECTION]
    experiments = await collection.distinct('id')
    return experiments


@experiment_router.get("/experiments/{experiment_id}", response_model=Experiment)
async def get_experiments(experiment_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][EXPERIMENT_COLLECTION]
    experiment = await collection.find_one({'id': experiment_id})
    if not experiment:
        raise HTTPException(status_code=404, detail=f"Experiment with id '{experiment_id}' not found")
    return experiment


@experiment_router.put("/experiments/{experiment_id}", response_model=Experiment)
async def update_experiments(experiment_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][EXPERIMENT_COLLECTION]
    experiment = await collection.find_one({'id': experiment_id})
    if not experiment:
        raise HTTPException(status_code=404, detail=f"Experiment with id '{experiment_id}' not found")
    experiment.update(**data)
    return experiment

