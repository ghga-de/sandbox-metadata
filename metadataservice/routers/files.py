from typing import List

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException

from metadataservice.schemas.file import File
from metadataservice.routers import DB_NAME, MONGODB_URL

FILE_COLLECTION = "files"

file_router = APIRouter()


@file_router.get("/files", response_model=List[str])
async def get_all_files():
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[DB_NAME][FILE_COLLECTION]
    files = await collection.distinct('id')
    return files


@file_router.get("/files/{file_id}", response_model=File)
async def get_files(file_id: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][FILE_COLLECTION]
    file = await collection.find_one({'id': file_id})
    if not file:
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found")
    return file


@file_router.put("/files/{file_id}", response_model=File)
async def update_files(file_id: str, data: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    collection = client[DB_NAME][FILE_COLLECTION]
    file = await collection.find_one({'id': file_id})
    if not file:
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found")
    file.update(**data)
    return file

