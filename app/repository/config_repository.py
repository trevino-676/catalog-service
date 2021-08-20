from bson import ObjectId

from app.model import ConfigModel
from app import app


class ConfigRepository:
    def save(self, document: dict):
        try:
            config = ConfigModel(document)
            config.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def get_one(self, filters: dict) -> ConfigModel:
        try:
            config = ConfigModel()
            config.find(filters)
            return config
        except Exception as e:
            app.logger.error(e)
            return None

    def update(self, document: dict):
        if "_id" in document:
            return False

        document["_id"] = (
            document["_id"]
            if isinstance(document["_id"], ObjectId)
            else ObjectId(document["_id"])
        )

        try:
            updated_document = ConfigModel(document)
            updated_document.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def delete(self, id: str):
        try:
            config = ConfigModel()
            config.find({"_id": ObjectId(id)})
            if not config:
                return False
            config.remove()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def get_all(self, filters):
        print(filters)
        return []
