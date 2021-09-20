import json

import pytest
import requests

from app import app


@pytest.fixture
def headers():
    payload = {"username": "test@sonar.com", "password": "test123"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(
        "https://www.sonar32.com.mx/auth", data=json.dumps(payload), headers=headers
    )
    headers["Authorization"] = f"jwt {res.json()['access_token']}"
    return headers


def test_create_config(headers):
    test_app = app.test_client()
    config = {"main_company": "TECO000101X00", "period": "monthly"}
    response = test_app.post("/v1/config/", data=json.dumps(config), headers=headers)

    assert response.status_code == 200
    assert response.json["status"] is True


def test_get_configuration(headers):
    test_app = app.test_client()
    response = test_app.get("/v1/config/", headers=headers)

    assert response.status_code == 200
    assert response.json["status"] is True


def test_update_configuration(headers):
    test_app = app.test_client()
    config_resp = test_app.get("/v1/config/", headers=headers)
    config = config_resp.json["data"]

    config["main_company"] = "PGT190401156"
    response = test_app.put("/v1/config/", data=json.dumps(config), headers=headers)

    assert response.status_code == 200
    assert response.json["status"] is True


def test_zdelete_configuration(headers):
    test_app = app.test_client()
    config_resp = test_app.get("/v1/config/", headers=headers)
    config = config_resp.json["data"]

    response = test_app.delete(f"/v1/config/{config['_id']}", headers=headers)

    assert response.status_code == 200
    assert response.json["status"] is True
