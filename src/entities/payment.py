from pydantic import BaseModel

class Payment(BaseModel):
    product_name: str
    product_description: str
    amount: float  
    currency: str = "brl"
    quantity: int = 1
    customer_email: str
    success_url: str
    cancel_url: str
