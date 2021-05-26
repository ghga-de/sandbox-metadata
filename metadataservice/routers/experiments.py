from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadataservice.schemas.experiment import Experiment
from metadataservice.routers import DB_NAME, MONGODB_URL

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

