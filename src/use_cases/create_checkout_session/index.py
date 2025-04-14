from fastapi import APIRouter, HTTPException, status
from use_cases.create_checkout_session.create_checkout_session_dto import CreateCheckoutSessionDTO
from use_cases.create_checkout_session.create_checkout_session_use_case import CreateCheckoutSessionUseCase
from repositories.payment_repository import PaymentRepository

router = APIRouter()

payment_repository = PaymentRepository()
create_checkout_session_use_case = CreateCheckoutSessionUseCase(repository=payment_repository)

@router.post("/create-checkout-session")
def create_checkout_session(dto: CreateCheckoutSessionDTO):
    try:
        result = create_checkout_session_use_case.execute(dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
