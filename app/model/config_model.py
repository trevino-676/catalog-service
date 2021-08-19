from app.model import DTO
from app import app, mongo


class ConfigModel(DTO):
    collection_name = app.config["CONFIG_COLLECTION"]
    collection = mongo.db[collection_name]
