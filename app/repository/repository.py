"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase abstracta para el repository
"""
from abc import ABC, abstractmethod

from app.model import User, Company, Suppliers, Payments


class Repository(ABC):
    @abstractmethod
    def save_user(self, user: dict) -> bool:
        pass

    @abstractmethod
    def get_user(self, filter: dict) -> User:
        pass

    @abstractmethod
    def update_user(self, user: dict) -> bool:
        pass

    @abstractmethod
    def delete_user(self, id: str) -> str:
        pass

    @abstractmethod
    def get_users(self, filter: dict) -> list:
        pass


class CompanyRepository(ABC):
    @abstractmethod
    def save(self, document: dict) -> bool:
        pass

    @abstractmethod
    def get_one(self, filter: dict) -> Company:
        pass

    @abstractmethod
    def update(self, document: dict) -> bool:
        pass

    @abstractmethod
    def delete(self, id: str) -> str:
        pass

    @abstractmethod
    def get_all(self, filter: dict) -> list:
        pass


class SupplierRepository(ABC):
    # @abstractmethod
    # def save(self, document: dict) -> bool:
    #     pass

    @abstractmethod
    def get_one(self, filter: dict) -> Suppliers:
        pass

    # @abstractmethod
    # def update(self, document: dict) -> bool:
    #     pass

    # @abstractmethod
    # def delete(self, id: str) -> str:
    #     pass

    @abstractmethod
    def get_all(self, filter: dict) -> list:
        pass

    @abstractmethod
    def update_one(self, filter:dict, values:dict):
        pass

class PaymentRepository(ABC):

    @abstractmethod
    def get_one(self, filter: dict) -> Payments:
        pass

    @abstractmethod
    def get_all(self, filter: dict) -> list:
        pass

    @abstractmethod
    def find_agg(self, filter:dict) -> list:
        pass
