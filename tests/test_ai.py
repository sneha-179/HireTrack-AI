import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def get_token():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "aitest@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "aitest@test.com",
        "password": "test1234"
    })
    return response.json()["access_token"]


def test_match_score_invalid_application():
    token = get_token()
    response = client.post("/ai/match/99999/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_match_score_invalid_resume():
    token = get_token()
    create = client.post("/applications/", json={
        "company": "Google",
        "role": "Backend Intern",
        "job_description": "Python FastAPI developer",
        "notes": "Applied via LinkedIn"
    }, headers={"Authorization": f"Bearer {token}"})
    app_id = create.json()["application_id"]
    response = client.post(f"/ai/match/{app_id}/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"


def test_skillgap_invalid_application():
    token = get_token()
    response = client.post("/ai/skillgap/99999/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_skillgap_invalid_resume():
    token = get_token()
    create = client.post("/applications/", json={
        "company": "Microsoft",
        "role": "Backend Intern",
        "job_description": "Python Django developer",
        "notes": "Applied via website"
    }, headers={"Authorization": f"Bearer {token}"})
    app_id = create.json()["application_id"]
    response = client.post(f"/ai/skillgap/{app_id}/99999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"