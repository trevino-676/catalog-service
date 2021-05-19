"""
author: Luis Manuel Torres Trevino
date: 18/05/2021
"""
from app.repository import CompanyRepository
from app.service.service import CService


class CompanyService(CService):
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def add(self, document: dict) -> bool:
        return self.repository.save(document)

    def get_one(self, filters: dict) -> dict:
        return self.repository.get_one(filters)

    def get_all(self, filters: dict) -> list:
        return self.repository.get_all(filters)

    def update(self, documnet: dict) -> bool:
        return self.repository.update(documnet)

    def delete(self, id: str) -> str:
        return self.repository.delete(id)