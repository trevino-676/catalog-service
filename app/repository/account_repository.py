from typing import Optional

from bson import ObjectId

from app import app
from app.model import AccountModel


class AccountRepository:
    def save(self, document: dict) -> bool:
        try:
            account = AccountModel(document)
            account.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def get_one(self, filters: dict) -> Optional[AccountModel]:
        try:
            account = AccountModel()
            account.find(filters)
            return account
        except Exception as e:
            app.logger.error(e)
            return None

    def get_all(self, filters: dict) -> Optional[list]:
        accounts = AccountModel.find_accounts(filters)
        return accounts

    def update(self, document: dict) -> bool:
        if "_id" in document:
            if "$oid" in document["_id"]:
                document["_id"] = ObjectId(document["_id"]["$oid"]) 
            if type(document["_id"]) is str:
                document["_id"] = ObjectId(document["_id"])

        try:
            account = AccountModel(document)
            account.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def delete(self, id: str) -> bool:
        filters = {"_id": ObjectId(id)}
        try:
            account = AccountModel()
            account.find(filters)
            if not account:
                return False
            account.remove()
            return True
        except Exception as e:
            app.logger.error(e)
            return False
