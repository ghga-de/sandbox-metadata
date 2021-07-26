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

COLLECTION_NAME = "file"


async def retrieve_files():
    collection = await get_collection(COLLECTION_NAME)
    files = await collection.distinct('id')
    return files


async def get_file(file_id):
    collection = await get_collection(COLLECTION_NAME)
    file = await collection.find_one({'id': file_id})
    if not file:
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found")
    return file


async def add_file(data: Dict):
    collection = await get_collection(COLLECTION_NAME)
    file_id = data['id']
    r = await collection.insert_one(data)
    file = await get_file(file_id)
    return file


async def update_file(file_id: str, data: Dict):
    file = await get_file(file_id)
    file.update(**data)
    return file
