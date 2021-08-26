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
"""Convenience methods for adding, updating, and retrieving Experiment objects"""

from typing import List
from fastapi.exceptions import HTTPException

from metadata_service.core.utils import embed_references
from metadata_service.database import DBConnect
from metadata_service.models import Experiment

COLLECTION_NAME = Experiment.__collection__
PREFIX = "EXP"


async def retrieve_experiments() -> List[Experiment]:
    """
    Retrieve a list of Experiments from metadata store.

    Returns:
        A list of Experiment objects.

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    experiments = await collection.find().to_list(None)  # type: ignore
    await db_connect.close_db()
    return experiments


async def get_experiment(experiment_id: str, embedded: bool = False) -> Experiment:
    """
    Given an Experiment ID, get the Experiment object from metadata store.

    Args:
        experiment_id: The Experiment ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
        The Experiment object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    experiment = await collection.find_one({"id": experiment_id})  # type: ignore
    if not experiment:
        raise HTTPException(
            status_code=404,
            detail=f"{Experiment.__name__} with id '{experiment_id}' not found",
        )
    if embedded:
        experiment = await embed_references(experiment, Experiment)
    await db_connect.close_db()
    return experiment


async def add_experiment(data: Experiment) -> Experiment:
    """
    Add an Experiment object to the metadata store.

    Args:
        data: The Experiment object

    Returns:
        The added Experiment object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    experiment_id = await db_connect.get_next_id(COLLECTION_NAME, PREFIX)
    data.id = experiment_id
    await collection.insert_one(data.dict())  # type: ignore
    await db_connect.close_db()
    experiment = await get_experiment(experiment_id)
    return experiment


async def update_experiment(experiment_id: str, data: Experiment) -> Experiment:
    """
    Given an Experiment ID and data, update the Experiment in metadata store.

    Args:
        experiment_id: The Experiment ID
        data: The Experiment object

    Returns:
        The updated Experiment object

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(COLLECTION_NAME)
    await collection.update_one({"id": experiment_id}, {"$set": data.dict()})  # type: ignore
    await db_connect.close_db()
    experiment = await get_experiment(experiment_id)
    return experiment
