"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase que implementa al servicio
"""
from app.repository import Repository
from app.service.service import Service


class UserService(Service):
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_user(self, user: dict) -> bool:
        return self.repository.save_user(user)

    def get_user(self, filters: dict):
        return self.repository.get_user(filters)

    def get_users(self, filters: dict) -> list:
        return self.repository.get_users(filters)

    def update_user(self, user: dict) -> bool:
        return self.repository.update_user(user)

    def delete_user(self, id: str) -> str:
        return self.repository.delete_user(id)