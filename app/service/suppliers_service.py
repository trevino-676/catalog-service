"""
author: ErrataSEV
date: 21/07/2021
"""
from app.repository import SupplierRepository
from app.service.service import SService


class SuppliersService(SService):
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def get_supp(self, filters: dict) -> dict:
        return self.repository.get_one(filters)
        
    def get_supps(self, filters: dict) -> list:
        return self.repository.get_all(filters)
    
    def update_one(self, filters: str, update: dict):
        return self.repository.update_one(filters, update)
