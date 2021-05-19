from app.repository import urepository, s3_repository, company_repository
from app.service.user_service import UserService
from app.service.upload_files_service import UploadFilesService
from app.service.company_service import CompanyService

user_service = UserService(urepository)
upload_service = UploadFilesService(s3_repository)
company_service = CompanyService(company_repository)