from pydantic import BaseModel

class PaymentModel(BaseModel):
    session_id: str
    session_url: str
