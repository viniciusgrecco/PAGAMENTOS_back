from repositories.payment_repository import PaymentRepository
from use_cases.create_pix_payment.create_pix_payment_dto import CreatePixPaymentDTO
from models.payment_model import PaymentModel

class CreatePixPaymentUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, data: CreatePixPaymentDTO) -> PaymentModel:
        # Aqui, os campos token e CPF não são necessários
        return self.repository.create_payment(data)
