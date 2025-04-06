# use_cases/create_card_payment/create_card_payment_use_case.py
from repositories.payment_repository import PaymentRepository
from use_cases.create_card_payment.create_card_payment_dto import CreateCardPaymentDTO
from models.payment_model import PaymentModel

class CreateCardPaymentUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, data: CreateCardPaymentDTO) -> PaymentModel:
        # Os campos token e CPF serão enviados junto com os dados do pagamento
        return self.repository.create_payment(data)
