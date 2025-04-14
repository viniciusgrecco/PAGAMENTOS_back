from entities.payment import Payment
from repositories.payment_repository import PaymentRepository
from use_cases.create_checkout_session.create_checkout_session_dto import CreateCheckoutSessionDTO

class CreateCheckoutSessionUseCase:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def execute(self, dto: CreateCheckoutSessionDTO) -> dict:
        payment = Payment(amount=dto.amount)
        return self.repository.create_checkout_session(payment, dto.payment_method)
