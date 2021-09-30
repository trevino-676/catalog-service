from app.repository import AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repo = repository

    def add(self, document: dict) -> bool:
        return self.repo.save(document)

    def get_one(self, filters: dict):
        return self.repo.get_one(filters)

    def get_all(self, filters: dict):
        return self.repo.get_all(filters)

    def update(self, document: dict):
        return self.repo.update(document)

    def delete(self, id: str):
        return self.repo.delete(id)
