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
"""
Utils
"""
import logging
from typing import Dict
from pydantic import BaseModel
from metadata_service.database import DBConnect


async def _get_reference(document_id: str, collection_name: str) -> Dict:
    """Given a document ID and a collection name, query the metadata store
    and return the document.

    Args:
        document_id: The ID of the document
        collection_name: The collection in the metadata store that has the document

    Returns
        The document corresponding to ``document_id``

    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=collection_name)
    doc = await collection.find_one({"id": document_id})  # type: ignore
    if not doc:
        logging.warning(
            "Reference with ID %s not found in collection %s",
            document_id,
            collection_name,
        )
    return doc


async def embed_references(parent_document: Dict, document_type: BaseModel) -> Dict:
    """Given a document and a document type, identify the references in ``parent_document``
    and query the metadata store. After retrieving the referenced objects, embed them in place
    of the reference in the parent document.

    Args:
        parent_document: The parent document that has one or more references
        document_type: An instance of ``pydantic.BaseModel``

    Returns
        The denormalize/embedded document

    """
    for field, referenced_obj in document_type.__references__:
        if field in parent_document and parent_document[field]:
            if isinstance(parent_document[field], str):
                referenced_doc = await _get_reference(
                    parent_document[field], referenced_obj.__collection__
                )
                referenced_doc = await embed_references(referenced_doc, referenced_obj)
                parent_document[field] = referenced_doc
            elif isinstance(parent_document[field], (list, set, tuple)):
                docs = []
                for ref in parent_document[field]:
                    referenced_doc = await _get_reference(
                        ref, referenced_obj.__collection__
                    )
                    referenced_doc = await embed_references(
                        referenced_doc, referenced_obj
                    )
                    docs.append(referenced_doc)
                parent_document[field] = docs
            else:
                raise ValueError(
                    f"Unexpected value type for field {field} in parent object {parent_document}"
                )
    return parent_document
