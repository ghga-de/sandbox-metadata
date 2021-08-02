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

from typing import List, Dict
from fastapi import APIRouter

from metadata_service.dao.file import retrieve_files, get_file, add_file, update_file
from metadata_service.models import File


file_router = APIRouter()


@file_router.get("/files", response_model=List[str], summary="Get all File IDs")
async def get_all_files():
    """Retrieve a list of File IDs from metadata store."""
    files = await retrieve_files()
    return files


@file_router.get("/files/{file_id}", response_model=File, summary="Get a File")
async def get_files(file_id: str, embedded: bool = False):
    """Given a File ID, get the File object from metadata store."""
    file = await get_file(file_id, embedded)
    return file


@file_router.post("/files", response_model=File, summary="Add a File")
async def add_files(data: Dict):
    """Add a File to the metadata store."""
    experiment = await add_file(data)
    return experiment


@file_router.put("/files/{file_id}", response_model=File, summary="Update a File")
async def update_files(file_id: str, data: dict):
    """Given a File ID and data, update the File object in metadata store."""
    file = await update_file(file_id, data)
    return file
