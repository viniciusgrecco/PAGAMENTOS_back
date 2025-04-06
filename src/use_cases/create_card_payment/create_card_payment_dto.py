# use_cases/create_card_payment/create_card_payment_dto.py
from pydantic import BaseModel

class CreateCardPaymentDTO(BaseModel):
    transaction_amount: float
    description: str
    payer_email: str
    payment_method_id: str  # deve ser "credit_card" ou "debit_card"
    token: str             # token do cartão
    payer_cpf: str         # CPF do pagador
