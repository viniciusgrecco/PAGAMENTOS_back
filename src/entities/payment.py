from pydantic import BaseModel

class Payment(BaseModel):
    amount: float
    currency: str = "brl"
    description: str = "Doação"
