from app.repository.repository import Repository, CompanyRepository, SupplierRepository
from app.repository.user_repository import UserMongoRepository
from app.repository.aws_repository import AWSRepository
from app.repository.company_repository import CompanyMongoRepository
from app.repository.suppliers_repository import SuppliersMongoRepository

urepository = UserMongoRepository()
s3_repository = AWSRepository()
company_repository = CompanyMongoRepository()
supp_repo = SuppliersMongoRepository()
