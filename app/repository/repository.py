"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase abstracta para el repository
"""
from abc import ABC, abstractmethod

from app.model import User


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
