from fastapi import APIRouter
from repositories.payment_repository import PaymentRepository
from use_cases.create_card_payment.create_card_payment_use_case import CreateCardPaymentUseCase
from use_cases.create_card_payment.create_card_payment_dto import CreateCardPaymentDTO

router = APIRouter()

@router.post("/create_payment/card")
async def create_card_payment(data: CreateCardPaymentDTO):
    repository = PaymentRepository()
    use_case = CreateCardPaymentUseCase(repository)
    return use_case.execute(data)
