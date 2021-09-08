"""
author: ErrataSEV
date: 18/08/2021
"""
from app.model import Payments
from app.repository import PaymentRepository
from app import app


class PaymentsMongoRepository(PaymentRepository):
    def get_one(self, filters: dict) -> dict:
        """
        Busca el datos del complemento de pago en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: diccionario con el documento encontrado.
        """
        try:
            payment = Payments()
            payment.find(filters)
            app.logger.info(f"Se encontro el complemento {str(payment._id)}")
            return payment
        except Exception as e:
            print("ERROR in repo", e)
            app.logger.error(e)
            return None

    def get_all(self, filters: dict) -> list:
        """
        Busca los complementos de pago de acuerdo a los filtros dados
        :param filters: diccionario con los filtros de busqueda
        :return: lista con todos los complementos correspondientes
        """
        try:
            payments = Payments.find_all(filters)
            app.logger.info(f"Se encontraron {len(payments)} documentos")
            return payments
        except Exception as e:
            app.logger.error(e)
            return None

    def find_agg(self, filters: list):
        """
        Realiza una busqueda con aggregate
        :param filters: lista de 'Stages' del aggregate
        :return: uknown
        """
        try:
            payments = Payments.find_agg(filters)
            app.logger.info(f"Respuesta {payments}")
            return payments
        except Exception as e:
            app.logger.error(e)
            return None
