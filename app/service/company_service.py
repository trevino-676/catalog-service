"""
author: Luis Manuel Torres Trevino
date: 18/05/2021
"""
from app.repository import CompanyRepository
from app.service.service import CService
from app import app


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

    def get_companies_by_user(self, user: dict) -> list:
        """
        Regresa las companias relacionadas con el usuario.
        """
        if "companies_info" in user:
            return user["companies_info"]

        filters = {"rfc": {"$in": user["companies"]}}
        return self.repository.get_all(filters)

    def update_files_company(self, rfc: str, document_type: str, filename: str):
        company = self.repository.get_one({"rfc": rfc})
        company[f"{document_type}_file"] = f"{rfc}/{filename}"
        company.save()

    def set_fiel_password(self, filters, fiel_password):
        try:
            company = self.repository.get_one(filters)
            company["fiel"] = fiel_password
            company.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False
