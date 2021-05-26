from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadataservice.schemas.study import Study
from metadataservice.routers import DB_NAME, MONGODB_URL

STUDY_COLLECTION = "studies"

studies_router = APIRouter()


@studies_router.get("/studies", response_model=List[str])
async def get_all_studies():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    studies = await collection.distinct('id')
    return studies


@studies_router.get("/studies/{study_id}", response_model=Study)
async def get_studies(study_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    study = await collection.find_one({'id': study_id})
    if not study:
        raise HTTPException(status_code=404, detail=f"Study with id '{study_id}' not found")
    return study


@studies_router.put("/studies/{study_id}", response_model=Study)
async def update_studies(study_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][STUDY_COLLECTION]
    study = await collection.find_one({'id': study_id})
    if not study:
        raise HTTPException(status_code=404, detail=f"Study with id '{study_id}' not found")
    study.update(**data)
    return study

