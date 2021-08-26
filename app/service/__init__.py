from bson import ObjectId

from app.repository import (
    urepository,
    s3_repository,
    company_repository,
    supp_repo,
    config_repo,
    pay_repo
)
from app.service.user_service import UserService
from app.service.upload_files_service import UploadFilesService
from app.service.company_service import CompanyService
from app.service.suppliers_service import SuppliersService
from app.service.config_service import ConfigService
from app.service.payments_service import PaymentService
from app.utils import check_password

user_service = UserService(urepository)
upload_service = UploadFilesService(s3_repository)
company_service = CompanyService(company_repository)
suppliers_service = SuppliersService(supp_repo)
config_service = ConfigService(config_repo)
pay_service = PaymentService(pay_repo)


def authenticate(email, password):
    filter = {"email": email}
    user = user_service.get_user(filter)
    user["id"] = str(user["_id"])
    for company in user.companies_info:
        company["_id"] = str(company["_id"])
    if user and check_password(password, user["password"]):
        return user


def identity(payload):
    identity = payload["identity"]
    id = identity if type(identity) == ObjectId else ObjectId(identity)
    return user_service.get_user({"_id": id})
