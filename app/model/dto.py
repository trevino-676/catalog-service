"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase base para todos los
    objetos dto del microservicio
"""
from abc import abstractmethod, ABC

class DTO(ABC):

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass
