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
import typer
import asyncio
import json
import motor.motor_asyncio


async def delete_all_records(db_url, db_name, collection_name):
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][collection_name]
    await collection.delete_many({})


def main(db_url: str = "mongodb://localhost:27017", db_name: str = "metadata"):
    typer.echo(f"Deleting all records from db {db_name} at URL {db_url}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_all_records(db_url, db_name, "study"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "publication"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "dataset"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "experiment"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "file"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "data_access_policy"))
    loop.run_until_complete(delete_all_records(db_url, db_name, "data_access_committee"))


if __name__ == "__main__":
    typer.run(main)
