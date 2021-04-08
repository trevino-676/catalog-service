"""
author: Luis Manuel Torre Trevino
description: Este archivo contien la clase abstracta para el servicio
"""
from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def add_user(self, user: dict) -> bool:
        pass

    @abstractmethod
    def get_user(self, filters: dict):
        pass

    @abstractmethod
    def get_users(self, filters: dict) -> list:
        pass

    @abstractmethod
    def update_user(self, user: dict) -> bool:
        pass

    @abstractmethod
    def delete_user(self, id: str) -> str:
        pass