from app.repository.repository import Repository, CompanyRepository
from app.repository.user_repository import UserMongoRepository
from app.repository.aws_repository import AWSRepository
from app.repository.company_repository import CompanyMongoRepository

urepository = UserMongoRepository()
s3_repository = AWSRepository()
company_repository = CompanyMongoRepository()
