from app.repository import urepository, s3_repository
from app.service.user_service import UserService
from app.service.upload_files_service import UploadFilesService

user_service = UserService(urepository)
upload_service = UploadFilesService(s3_repository)