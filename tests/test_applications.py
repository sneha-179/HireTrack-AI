import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "apptest@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "apptest@test.com",
        "password": "test1234"
    })
    return response.json()["access_token"]


def test_create_application():
    token = get_token()
    response = client.post("/applications/", json={
        "company": "Google",
        "role": "Backend Intern",
        "job_description": "Python FastAPI developer",
        "notes": "Applied via LinkedIn"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert "application_id" in response.json()


def test_get_all_applications():
    token = get_token()
    response = client.get("/applications/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_application():
    token = get_token()
    create = client.post("/applications/", json={
        "company": "Microsoft",
        "role": "Python Intern",
        "job_description": "Django developer",
        "notes": "Applied via website"
    }, headers={"Authorization": f"Bearer {token}"})
    app_id = create.json()["application_id"]
    response = client.get(f"/applications/{app_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["company"] == "Microsoft"


def test_update_application():
    token = get_token()
    create = client.post("/applications/", json={
        "company": "Amazon",
        "role": "Backend Intern",
        "job_description": "AWS developer",
        "notes": "Applied via LinkedIn"
    }, headers={"Authorization": f"Bearer {token}"})
    app_id = create.json()["application_id"]
    response = client.put(f"/applications/{app_id}", json={
        "status": "Interview"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Application updated successfully"


def test_filter_by_status():
    token = get_token()
    response = client.get("/applications/filter?status=Applied", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_application():
    token = get_token()
    create = client.post("/applications/", json={
        "company": "Meta",
        "role": "Backend Intern",
        "job_description": "Python developer",
        "notes": "Applied via LinkedIn"
    }, headers={"Authorization": f"Bearer {token}"})
    app_id = create.json()["application_id"]
    response = client.delete(f"/applications/{app_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Application deleted successfully"


def test_get_nonexistent_application():
    token = get_token()
    response = client.get("/applications/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404