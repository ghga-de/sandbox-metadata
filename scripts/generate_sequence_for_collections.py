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
    start up script for generating sequences for the metadata collections
"""

import asyncio
from typing import Literal, get_args
import typer
import motor.motor_asyncio

CollectionTypes = Literal[
    "study",
    "publication",
    "dataset",
    "file",
    "experiment",
    "data_access_policy",
    "data_access_committee",
]
COUNTER = "counter"


async def insert_records(db_url: str, db_name: str, collection_name: CollectionTypes):
    """Insert sequence for specific collection type"""

    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][COUNTER]
    await collection.insert_one({"_id": collection_name, "value": 0})


def main(db_url: str = "mongodb://localhost:27017", db_name: str = "metadata"):
    """
    Insert the sequence for the counter collection
    """
    loop = asyncio.get_event_loop()
    collections = get_args(CollectionTypes)
    for collection in collections:
        typer.echo(f'  - inserting sequence for collection: "{collection}"')
        loop.run_until_complete(insert_records(db_url, db_name, collection))

    typer.echo("Done.")


if __name__ == "__main__":
    typer.run(main)
