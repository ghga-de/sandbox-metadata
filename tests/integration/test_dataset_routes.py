"""
Test Dataset routes
"""
import pytest
from tests.fixtures import initialize_test_db, api_client


def test_get_dataset_route(initialize_test_db, api_client):
    """Test fetching dataset records from metadata store"""
    response = api_client.get("/datasets")
    assert response.status_code == 200
    dataset_list = [x["id"] for x in response.json()]
    assert isinstance(dataset_list, list)
    assert "DAT:0000001" in dataset_list
    assert "DAT:0000002" in dataset_list

    for item in dataset_list:
        response = api_client.get(f"/datasets/{item}")
        assert response.status_code == 200
        dataset = response.json()
        assert dataset["id"] in dataset_list
        assert "files" in dataset and dataset["title"] is not None


def test_add_dataset_route(initialize_test_db, api_client):
    """Test adding a dataset record to metadata store"""
    response = api_client.post(
        "/datasets", json={"id": "DAT:1234567", "title": "Test Dataset"}
    )
    assert response.status_code == 200
    dataset = response.json()
    assert "title" in dataset and dataset["title"] == "Test Dataset"

    response = api_client.get("/datasets/DAT:1234567")
    assert response.status_code == 404


def test_update_dataset_route(initialize_test_db, api_client):
    """Test updating a dataset record to metadata store"""
    response = api_client.put(
        "/datasets/DAT:0000002",
        json={"id": "DAT:0000002", "title": "Modified Dataset 2"},
    )
    assert response.status_code == 200

    response = api_client.get("/datasets/DAT:0000002")
    assert response.status_code == 200
    dataset = response.json()
    assert dataset["title"] == "Modified Dataset 2"
