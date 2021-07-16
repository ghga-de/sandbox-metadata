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

import asyncio
import json
import motor.motor_asyncio


async def insert_records(db_name, collection_name, records):
    client = motor.motor_asyncio.AsyncIOMotorClient()
    c = client[db_name][collection_name]
    await c.insert_many(records)


async def delete_all_records(db_name, collection_name):
    client = motor.motor_asyncio.AsyncIOMotorClient()
    c = client[db_name][collection_name]
    await c.delete_many({})


async def get_collection(db_name, collection_name):
    client = motor.motor_asyncio.AsyncIOMotorClient()
    c = client[db_name][collection_name]
    r = await c.distinct('_id')
    return r


DB_NAME = 'metadata'

study_records = json.load(open('examples/studies.json'))
publication_records = json.load(open('examples/publications.json'))
dataset_records = json.load(open('examples/datasets.json'))
experiment_records = json.load(open('examples/experiments.json'))
file_records = json.load(open('examples/files.json'))

loop = asyncio.get_event_loop()
loop.run_until_complete(delete_all_records(DB_NAME, 'study'))
loop.run_until_complete(delete_all_records(DB_NAME, 'publication'))
loop.run_until_complete(delete_all_records(DB_NAME, 'dataset'))
loop.run_until_complete(delete_all_records(DB_NAME, 'experiment'))
loop.run_until_complete(delete_all_records(DB_NAME, 'file'))


loop.run_until_complete(insert_records(DB_NAME, 'study', study_records['studies']))
loop.run_until_complete(insert_records(DB_NAME, 'publication', publication_records['publications']))
loop.run_until_complete(insert_records(DB_NAME, 'dataset', dataset_records['datasets']))
loop.run_until_complete(insert_records(DB_NAME, 'experiment', experiment_records['experiments']))
loop.run_until_complete(insert_records(DB_NAME, 'file', file_records['files']))

print(loop.run_until_complete(get_collection(DB_NAME, 'study')))
print(loop.run_until_complete(get_collection(DB_NAME, 'publication')))
print(loop.run_until_complete(get_collection(DB_NAME, 'dataset')))
print(loop.run_until_complete(get_collection(DB_NAME, 'experiment')))
print(loop.run_until_complete(get_collection(DB_NAME, 'file')))
