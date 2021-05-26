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
loop.run_until_complete(delete_all_records(DB_NAME, 'studies'))
loop.run_until_complete(delete_all_records(DB_NAME, 'publications'))
loop.run_until_complete(delete_all_records(DB_NAME, 'datasets'))
loop.run_until_complete(delete_all_records(DB_NAME, 'experiments'))
loop.run_until_complete(delete_all_records(DB_NAME, 'files'))


loop.run_until_complete(insert_records(DB_NAME, 'studies', study_records['studies']))
loop.run_until_complete(insert_records(DB_NAME, 'publications', publication_records['publications']))
loop.run_until_complete(insert_records(DB_NAME, 'datasets', dataset_records['datasets']))
loop.run_until_complete(insert_records(DB_NAME, 'experiments', experiment_records['experiments']))
loop.run_until_complete(insert_records(DB_NAME, 'files', file_records['files']))

print(loop.run_until_complete(get_collection(DB_NAME, 'studies')))
print(loop.run_until_complete(get_collection(DB_NAME, 'publications')))
print(loop.run_until_complete(get_collection(DB_NAME, 'datasets')))
print(loop.run_until_complete(get_collection(DB_NAME, 'experiments')))
print(loop.run_until_complete(get_collection(DB_NAME, 'files')))
