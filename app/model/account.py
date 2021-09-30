from typing import Optional

from app.model import DTO
from app import app, mongo


class AccountModel(DTO):
    collection_name = app.config.get("ACCOUNT_COLLECTION")
    collection = mongo.db[collection_name]

    @classmethod
    def find_accounts(cls, filters: dict) -> Optional[list]:
        """
        This method searchs the accounts that match with the filters.
        """
        try:
            accounts = cls.collection.find(filters)
            return list(accounts)
        except Exception as e:
            app.logger.error(e)
            return None
