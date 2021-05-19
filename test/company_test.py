"""
author: Luis Manuel Torres Trevino
date: 19/05/2021
"""
import unittest
import json

from app import app


class CompanyServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}
        self.company = {
            "name": "company_test",
            "rfc": "TECO000101X00",
            "users": [],
            "address": "cauncun. Qroo",
            "phone_number": "3312758869",
        }
        self.filters = {"type": "and", "filters": {"rfc": self.company["rfc"]}}

    def test_create_company(self):
        response = self.app.post(
            "/v1/company/", headers=self.headers, data=json.dumps({"company": self.company})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_find_company(self):
        response = self.app.get(
            "/v1/company/", headers=self.headers, data=json.dumps(self.filters)
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_find_companies(self):
        response = self.app.get(
            "v1/company/all", headers=self.headers, data=json.dumps(self.filters)
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_update_company(self):
        response_company = self.app.get(
            "/v1/company/", headers=self.headers, data=json.dumps(self.filters)
        )
        company = response_company.json["company"]
        company["address"] = "Guadalajara, Jalisco"
        company["_id"] = company["_id"]["$oid"]
        response = self.app.put(
            "/v1/company/", headers=self.headers, data=json.dumps({"company": company})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])

    def test_zdelete_company(self):
        response_company = self.app.get(
            "/v1/company/", headers=self.headers, data=json.dumps(self.filters)
        )
        company = response_company.json["company"]
        id = company["_id"]["$oid"]
        response = self.app.delete(f"/v1/company/{id}", headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json["status"])


if __name__ == "__main__":
    unittest.main()