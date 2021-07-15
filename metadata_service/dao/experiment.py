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

COLLECTION_NAME = "experiments"


async def retrieve_experiments():
    collection = get_collection(COLLECTION_NAME)
    experiments = await collection.distinct('id')
    return experiments


async def get_experiment(experiment_id):
    collection = get_collection(COLLECTION_NAME)
    experiment = await collection.find_one({'id': experiment_id})
    if not experiment:
        raise HTTPException(status_code=404, detail=f"Experiment with id '{experiment_id}' not found")
    return experiment


async def add_experiment(data: Dict):
    collection = get_collection(COLLECTION_NAME)
    experiment = await collection.insert_one(data)
    return experiment


async def update_experiment(experiment_id: str, data: Dict):
    experiment = await get_experiment(experiment_id)
    experiment.update(**data)
    return experiment
