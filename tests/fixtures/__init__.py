import os
import pymongo
import json
import pytest
from fastapi.testclient import TestClient
from metadata_service.api import app
from metadata_service.config import get_config
import mongomock


@pytest.fixture(scope="session")
@mongomock.patch(servers=(('localhost', 28017),))
def initialize_test_db():
    curr_dir = os.path.dirname(__file__)
    json_files = [
        ("datasets.json", "dataset"),
        ("studies.json", "study"),
        ("experiments.json", "experiment")
    ]
    client = pymongo.MongoClient('localhost:28017')
    for file, collection_name in json_files:
        objects = json.load(open(os.path.join(curr_dir, '..', '..', 'examples', file)))
        client['test-metadata'][collection_name].delete_many({})
        client['test-metadata'][collection_name].insert_many(objects[file.split(".")[0]])


@pytest.fixture(scope="function")
def initialize_test_db():
    """Initalize a test metadata store"""
    config = get_config()
    curr_dir = os.path.dirname(__file__)
    json_files = [
        ("datasets.json", "dataset"),
        ("studies.json", "study"),
        ("experiments.json", "experiment")
    ]
    for file, collection_name in json_files:
        objects = json.load(open(os.path.join(curr_dir, '..', '..', 'examples', file)))
        client = pymongo.MongoClient(config.db_url)
        client[config.db_name][collection_name].delete_many({})
        client[config.db_name][collection_name].insert_many(objects[file.split(".")[0]])


@pytest.fixture(scope="session")
def api_client():
    """Get an instance of TestClient"""
    client = TestClient(app)
    yield client
