from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadataservice.schemas.dataset import Dataset
from metadataservice.routers import DB_NAME, MONGODB_URL

DATASET_COLLECTION = "datasets"

dataset_router = APIRouter()


@dataset_router.get("/datasets", response_model=List[str])
async def get_all_datasets():
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[DB_NAME][DATASET_COLLECTION]
    datasets = await collection.distinct('id')
    return datasets


@dataset_router.get("/datasets/{dataset_id}", response_model=Dataset)
async def get_datasets(dataset_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][DATASET_COLLECTION]
    dataset = await collection.find_one({'id': dataset_id})
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset with id '{dataset_id}' not found")
    return dataset


@dataset_router.put("/datasets/{dataset_id}", response_model=Dataset)
async def update_datasets(dataset_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][DATASET_COLLECTION]
    dataset = await collection.find_one({'id': dataset_id})
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset with id '{dataset_id}' not found")
    dataset.update(**data)
    return dataset

