from fastapi import APIRouter, Request
from use_cases.stripe_webhook.stripe_webhook_use_case import StripeWebhookUseCase

router = APIRouter()

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    use_case = StripeWebhookUseCase()
    return await use_case.execute(request)