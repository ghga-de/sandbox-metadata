from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadata_service.schemas.publication import Publication
from metadata_service.routers import DB_NAME, MONGODB_URL

PUBLICATION_COLLECTION = "publications"

publication_router = APIRouter()


@publication_router.get("/publications", response_model=List[str])
async def get_all_publications():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publications = await collection.distinct('id')
    return publications


@publication_router.get("/publications/{publication_id}", response_model=Publication)
async def get_publications(publication_id):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publication = await collection.find_one({'id': publication_id})
    if not publication:
        raise HTTPException(status_code=404, detail=f"Publication with id '{publication_id}' not found")
    return publication


@publication_router.put("/publications/{publication_id}", response_model=Publication)
async def update_publications(publication_id, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][PUBLICATION_COLLECTION]
    publication = await collection.find_one({'id': publication_id})
    if not publication:
        raise HTTPException(status_code=404, detail=f"Publication with id '{publication_id}' not found")
    publication.update(**data)
    return publication

