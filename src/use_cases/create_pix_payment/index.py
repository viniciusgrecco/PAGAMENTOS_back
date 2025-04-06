# use_cases/create_pix_payment/index.py
from fastapi import APIRouter, Request
from repositories.payment_repository import PaymentRepository
from use_cases.create_pix_payment.create_pix_payment_use_case import CreatePixPaymentUseCase
from use_cases.create_pix_payment.create_pix_payment_dto import CreatePixPaymentDTO

router = APIRouter()

@router.post("/create_payment/pix")
async def create_pix_payment(request: Request):
    raw_body = await request.body()
    decoded_body = raw_body.decode("utf-8")
    print("DEBUG: Raw Request Body:", decoded_body)
    
    try:
        data = await request.json()
        print("DEBUG: JSON Data:", data)
    except Exception as e:
        print("DEBUG: Erro ao ler JSON:", e)
        return {"error": True, "message": "JSON inválido"}
    
    # Tente converter para o DTO manualmente
    try:
        payload = CreatePixPaymentDTO(**data)
    except Exception as e:
        print("DEBUG: Erro na validação do DTO:", e)
        return {"error": True, "message": f"Erro na validação: {e}"}
    
    repository = PaymentRepository()
    use_case = CreatePixPaymentUseCase(repository)
    return use_case.execute(payload)
