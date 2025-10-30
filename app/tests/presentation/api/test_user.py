import pytest
from faker import Faker
from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.asyncio
async def test_create_user_success(app: FastAPI, client: TestClient, faker: Faker):
    url = app.url_path_for("create_user_handler")
    payload = {
        "username": faker.user_name()[:50],
        "email": faker.email(),
        "telegram": "@" + faker.user_name(),
        "phone": "+1 (555) 123-4567",
    }
    response: Response = client.post(url=url, json=payload)

    assert response.status_code == status.HTTP_201_CREATED, response.json()

    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["telegram"] == payload["telegram"]
    assert data["phone"] == payload["phone"]


@pytest.mark.asyncio
async def test_create_user_fails_with_invalid_email(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for("create_user_handler")
    payload = {
        "username": "john_doe",
        "email": "invalid-email",
        "telegram": "@johnny",
        "phone": "+1 (555) 123-4567",
    }
    response: Response = client.post(url=url, json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"]["error"]


@pytest.mark.asyncio
async def test_create_user_fails_with_empty_username(app: FastAPI, client: TestClient):
    url = app.url_path_for("create_user_handler")
    payload = {
        "username": "",
        "email": "user@example.com",
        "telegram": "@johnny",
        "phone": "+1 (555) 123-4567",
    }
    response: Response = client.post(url=url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert response.json()["detail"]["error"]
