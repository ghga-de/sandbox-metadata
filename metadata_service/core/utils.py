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
import logging
from metadata_service.database import get_collection


async def _get_reference(object_id, collection_name):
    collection = await get_collection(collection_name)
    doc = await collection.find_one({"id": object_id})
    if not doc:
        logging.warning(f"Reference with ID {object_id} not found in collection {collection_name}")
    return doc


async def embed_references(parent_object, object_type):
    for field, referenced_obj in object_type.__references__:
        if field in parent_object and parent_object[field]:
            if isinstance(parent_object[field], str):
                referenced_doc = await _get_reference(parent_object[field], referenced_obj.__collection__)
                referenced_doc2 = await embed_references(referenced_doc, referenced_obj)
                parent_object[field] = referenced_doc2
            elif isinstance(parent_object[field], (list, set, tuple)):
                docs = []
                for ref in parent_object[field]:
                    referenced_doc = await _get_reference(ref, referenced_obj.__collection__)
                    referenced_doc2 = await embed_references(referenced_doc, referenced_obj)
                    docs.append(referenced_doc2)
                parent_object[field] = docs
            else:
                raise ValueError(f"Unexpected value type for field {field} in parent object {parent_object}")
    return parent_object
