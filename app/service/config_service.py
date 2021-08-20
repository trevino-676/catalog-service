from app.repository import CompanyRepository
from app.service.service import CService


class ConfigService(CService):
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def add(self, document: dict):
        return self.repository.save(document)

    def get_one(self, filters: dict):
        return self.repository.get_one(filters)

    def update(self, document: dict):
        return self.repository.update(document)

    def delete(self, id: str):
        return self.repository.delete(id)
