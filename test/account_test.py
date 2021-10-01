import json

import pytest
import requests

from app import app


test_app = app.test_client()


@pytest.fixture
def headers():
    payload = {"username": "test@sonar.com", "password": "test123"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(
        "https://www.sonar32.com.mx/auth", data=json.dumps(payload), headers=headers
    )
    headers["Authorization"] = f"jwt {res.json()['access_token']}"
    return headers


def test_create_account(headers):
    account = {"company": "MODA123456", "bank": "Santander", "account": "0001454761"}
    response = test_app.post("/v1/account/", data=json.dumps(account), headers=headers)

    assert response.status_code == 200
    assert response.json["status"] is True


def test_find_by_user(headers):
    response = test_app.get("/v1/account/by_user", headers=headers)

    assert response.status_code == 200
    assert len(response.json["data"]) > 0
    assert response.json["status"] is True


def test_update_account(headers):
    response = test_app.get("/v1/account/?company=MODA123456", headers=headers)
    account = response.json["data"]
    account["bank"] = "BBVA"
    resp = test_app.put("/v1/account/", data=json.dumps(account), headers=headers)

    assert resp.status_code == 200
    assert resp.json["status"] is True


def test_zdelete_account(headers):
    response = test_app.get("/v1/account/?company=MODA123456", headers=headers)
    account = response.json["data"]
    id = account["_id"]["$oid"]
    resp = test_app.delete(f"/v1/account/?id={id}", headers=headers)

    assert resp.status_code == 200
    assert resp.json["status"] is True

