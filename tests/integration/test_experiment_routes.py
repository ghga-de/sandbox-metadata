import pytest
from tests.fixtures import initialize_test_db, api_client


def test_get_experiment_route(initialize_test_db, api_client):
    """Test fetching experiment records from metadata store"""
    response = api_client.get("/experiments")
    assert response.status_code == 200
    experiment_list = [x["id"] for x in response.json()]
    assert isinstance(experiment_list, list)
    assert "EXP:0000001" in experiment_list
    assert "EXP:0000002" in experiment_list

    for item in experiment_list:
        response = api_client.get(f"/experiments/{item}")
        assert response.status_code == 200
        experiment = response.json()
        assert experiment["id"] in experiment_list


def test_add_experiment_route(initialize_test_db, api_client):
    """Test adding an experiment record to metadata store"""
    response = api_client.post(
        "/experiments", json={"id": "EXP:1234567", "name": "Test Experiment"}
    )
    assert response.status_code == 200
    experiment = response.json()
    assert "id" in experiment and experiment["name"] == "Test Experiment"

    response = api_client.get("/experiments/EXP:1234567")
    assert response.status_code == 404


def test_update_experiment_route(initialize_test_db, api_client):
    """Test update experiment records to metadata store"""
    response = api_client.put(
        "/experiments/EXP:0000002",
        json={"id": "EXP:0000002", "name": "Modified Experiment 2"},
    )
    assert response.status_code == 200

    response = api_client.get("/experiments/EXP:0000002")
    assert response.status_code == 200
    experiment = response.json()
    assert experiment["name"] == "Modified Experiment 2"
