"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase base para todos los
    objetos dto del microservicio
"""
from bson import ObjectId


class DTO(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delattr__
    __setattr__ = dict.__setattr__

    def save(self):
        if not self._id:
            self.collection.insert_one(self)
        else:
            self.collection.replace_one({"_id": ObjectId(self._id)}, self)

    def reload(self):
        if self._id:
            self.update(self.collection.find_one({"_id": ObjectId(self.__id)}))

    def remove(self):
        if self._id:
            self.collection.delete_one({"_id": ObjectId(self._id)})
            self.clear()

    def find(self, filters: dict):
        if dict is not None:
            self.update(self.collection.find_one(filters))
