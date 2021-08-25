"""
    Fixtures for metadata
"""
import os
import json
import pymongo
import pytest
import mongomock
from fastapi.testclient import TestClient
from metadata_service.api import app


@pytest.fixture(scope="session")
@mongomock.patch(servers=(("localhost", 28017),))
def initialize_test_db():
    """Initialize a test metadata store using mongomock"""
    curr_dir = os.path.dirname(__file__)
    json_files = [
        ("datasets.json", "dataset"),
        ("studies.json", "study"),
        ("experiments.json", "experiment"),
    ]
    client = pymongo.MongoClient("localhost:28017")
    for file, collection_name in json_files:
        objects = json.load(open(os.path.join(curr_dir, "..", "..", "examples", file)))
        client["test-metadata"][collection_name].delete_many({})
        client["test-metadata"][collection_name].insert_many(
            objects[file.split(".")[0]]
        )


@pytest.fixture(scope="session")
def api_client():
    """Get an instance of TestClient"""
    client = TestClient(app)
    yield client
