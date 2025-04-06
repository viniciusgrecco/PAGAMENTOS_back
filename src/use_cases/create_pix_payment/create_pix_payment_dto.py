from pydantic import BaseModel

class CreatePixPaymentDTO(BaseModel):
    transaction_amount: float
    description: str
    payer_email: str
    payment_method_id: str = "pix"  
