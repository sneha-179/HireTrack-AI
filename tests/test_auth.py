import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_success():
    response = client.post("/auth/register", json={
        "name": "Sneha",
        "email": "newuser@test.com",
        "password": "test1234"
    })
    assert response.status_code == 201
    assert "user_id" in response.json()


def test_register_duplicate_email():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "duplicate@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/register", json={
        "name": "Sneha",
        "email": "duplicate@test.com",
        "password": "test1234"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "login@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "test1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_wrong_email():
    response = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "test1234"
    })
    assert response.status_code == 401


def test_logout():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "logout@test.com",
        "password": "test1234"
    })
    login = client.post("/auth/login", json={
        "email": "logout@test.com",
        "password": "test1234"
    })
    token = login.json()["access_token"]
    response = client.get("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_get_profile():
    client.post("/auth/register", json={
        "name": "Sneha",
        "email": "profile@test.com",
        "password": "test1234"
    })
    login = client.post("/auth/login", json={
        "email": "profile@test.com",
        "password": "test1234"
    })
    token = login.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "profile@test.com"