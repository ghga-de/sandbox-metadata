import pytest
from tests.fixtures import initialize_test_db, api_client


@pytest.mark.skip()
def test_get_study_route(initialize_test_db, api_client):
    """Test fetching study records from metadata store"""
    response = api_client.get('/studies')
    assert response.status_code == 200
    study_list = response.json()
    assert isinstance(study_list, list)
    assert 'STU:0000001' in study_list
    assert 'STU:0000002' in study_list

    for study_id in study_list:
        response = api_client.get(f'/studies/{study_id}')
        assert response.status_code == 200
        study = response.json()
        assert study['id'] in study_list
        assert 'publications' in study and study['publications'] is not None


@pytest.mark.skip()
def test_add_study_route(initialize_test_db, api_client):
    """Test adding study records to metadata store"""
    response = api_client.post('/studies', json={"id": "STU:1234567", "title": "Test study"})
    assert response.status_code == 200
    study = response.json()
    assert "id" in study and study["id"] == "STU:1234567"

    response = api_client.get("/studies/STU:1234567")
    assert response.status_code == 200
    study = response.json()
    assert study["title"] == "Test study"


@pytest.mark.skip()
def test_update_study_route(initialize_test_db, api_client):
    """Test update study records to metadata store"""
    response = api_client.put('/studies/STU:0000002', json={"id": "STU:0000002", "title": "Modified Study 2"})
    assert response.status_code == 200

    response = api_client.get("/studies/STU:0000002")
    assert response.status_code == 200
    study = response.json()
    assert study["title"] == "Modified Study 2"
