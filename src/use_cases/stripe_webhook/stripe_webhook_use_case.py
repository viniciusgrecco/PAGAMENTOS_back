import os
import json
import datetime
import stripe
from fastapi import Request, HTTPException
from repositories.payment_repository import PaymentRepository

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

class StripeWebhookUseCase:
    def __init__(self):
        self.payment_repository = PaymentRepository()

    async def execute(self, request: Request):
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Payload inválido")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Assinatura inválida")

        print(f"evento recebido: {event['type']}")
        print("Payload recebido:", json.dumps(event, indent=2))

        def get_payment_id(data):
            return data.get("metadata", {}).get("internal_payment_id")

        if event["type"] == "payment_intent.succeeded":
            pi = event["data"]["object"]
            internal_id = get_payment_id(pi)
            if internal_id:
                self.payment_repository.update_payment_status(
                    payment_id=internal_id,
                    status="succeeded"
                )

        elif event["type"] == "payment_intent.payment_failed":
            pi = event["data"]["object"]
            internal_id = get_payment_id(pi)
            if internal_id:
                self.payment_repository.update_payment_status(
                    payment_id=internal_id,
                    status="failed"
                )

        elif event["type"] == "payment_intent.processing":
            pi = event["data"]["object"]
            internal_id = get_payment_id(pi)
            if internal_id:
                self.payment_repository.update_payment_status(
                    payment_id=internal_id,
                    status="processing"
                )

        elif event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            internal_id = get_payment_id(session)
            if internal_id:
                created = session.get("created")
                try:
                    updated_at = datetime.datetime.fromtimestamp(float(created), datetime.timezone.utc)
                except Exception:
                    updated_at = datetime.datetime.now(datetime.timezone.utc)

                self.payment_repository.update_payment_status(
                    payment_id=internal_id,
                    status="succeeded",
                    updated_at=updated_at
                )

        return {"status": "success"}