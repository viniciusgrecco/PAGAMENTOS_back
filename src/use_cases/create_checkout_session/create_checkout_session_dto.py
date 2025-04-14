from pydantic import BaseModel

class CreateCheckoutSessionDTO(BaseModel):
    amount: float
    payment_method: str 
