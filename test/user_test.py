import unittest
import json
import base64

from app import app
from app.service import user_service


class UserServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def test_create_user(self):
        payload = {
            "name": "user",
            "last_name": "test",
            "email": "user_test@test.com",
            "rfc": "TEUS000101X00",
            "password": "test123",
        }
        response = self.app.post(
            "/v1/user/", headers=self.headers, data=json.dumps(payload)
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_find_user(self):
        payload = {"name": "user", "rfc": "TEUS000101X00"}
        response = self.app.get(
            "/v1/user/", headers=self.headers, data=json.dumps(payload)
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("test", response.json["user"]["last_name"])
        self.assertEqual(True, response.json["status"])

    def test_update_user(self):
        payload = {"name": "user", "rfc": "TEUS000101X00"}
        resp = self.app.get("/v1/user/", headers=self.headers, data=json.dumps(payload))
        user = resp.json["user"]
        user["email"] = "test@test.com"
        response = self.app.put(
            "/v1/user/", headers=self.headers, data=json.dumps(user)
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_zdelete_user(self):
        response = self.app.get(
            "/v1/user/", headers=self.headers, data=json.dumps({"rfc": "TEUS000101X00"})
        )
        payload = {"_id": response.json["user"]["_id"]}
        resp = self.app.delete(
            "/v1/user/", headers=self.headers, data=json.dumps(payload)
        )
        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])

    def test_update_file_route(self):
        payload = {
            "rfc": "TEUS000101X00",
            "filename_cer": "test.cer",
            "filename_key": "test.key",
        }
        user_service.update_files_user(payload["rfc"], "cer", payload["filename_cer"])
        user_service.update_files_user(payload["rfc"], "key", payload["filename_key"])

        resp = self.app.get(
            "/v1/user/", headers=self.headers, data=json.dumps({"rfc": payload["rfc"]})
        )

        self.assertEqual(
            f"{payload['rfc']}/{payload['filename_cer']}", resp.json["user"]["cer"]
        )
        self.assertEqual(
            f"{payload['rfc']}/{payload['filename_key']}", resp.json["user"]["key"]
        )

    def test_set_fiel_password(self):
        payload = {
            "rfc": "TEUS000101X00",
            "fiel": "hola",
        }
        resp = self.app.post(
            "/v1/user/fiel", headers=self.headers, data=json.dumps(payload)
        )

        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json["status"])


if __name__ == "__main__":
    unittest.main()
