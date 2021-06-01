from bson import ObjectId

from app.repository import urepository, s3_repository, company_repository
from app.service.user_service import UserService
from app.service.upload_files_service import UploadFilesService
from app.service.company_service import CompanyService
from app.utils import check_password

user_service = UserService(urepository)
upload_service = UploadFilesService(s3_repository)
company_service = CompanyService(company_repository)


def authenticate(email, password):
    filter = {"email": email}
    user = user_service.get_user(filter)
    user["id"] = str(user["_id"])
    if user and check_password(password, user["password"]):
        return user


def identity(payload):
    identity = payload["identity"]
    id = identity if type(identity) == ObjectId else ObjectId(identity)
    return user_service.get_user({"_id": id})