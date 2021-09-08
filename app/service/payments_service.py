"""
author: ErrataSEV
date: 18/08/2021
"""
from app.repository import PaymentRepository
from app.service.service import PayCompService


class PaymentService(PayCompService):
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def get_pay(self, filters: dict) -> dict:
        return self.repository.get_one(filters)

    def get_pays(self, filters: dict) -> list:
        return self.repository.get_all(filters)

    def find_agg(self, filters: list):
        return self.repository.find_agg(filters)
