from app.repository.repository import Repository
from app.repository.user_repository import UserMongoRepository
from app.repository.aws_repository import AWSRepository

urepository = UserMongoRepository()
s3_repository = AWSRepository()