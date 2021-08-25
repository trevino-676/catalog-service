from app.model.payments_model import Payments
from app.repository.repository import Repository, CompanyRepository, SupplierRepository, PaymentRepository
from app.repository.user_repository import UserMongoRepository
from app.repository.aws_repository import AWSRepository
from app.repository.company_repository import CompanyMongoRepository
from app.repository.suppliers_repository import SuppliersMongoRepository
from app.repository.config_repository import ConfigRepository
from app.repository.payments_repository import PaymentsMongoRepository

urepository = UserMongoRepository()
s3_repository = AWSRepository()
company_repository = CompanyMongoRepository()
supp_repo = SuppliersMongoRepository()
config_repo = ConfigRepository()
pay_repo = PaymentsMongoRepository()