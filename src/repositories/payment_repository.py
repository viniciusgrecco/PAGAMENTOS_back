import os
import datetime
from entities.payment import Payment
from integrations.mercadopago_integration import create_mercadopago_checkout_preference
from integrations.stripe_integration import create_stripe_checkout_session
from models.payment_model import PaymentModel

class PaymentRepository:
    def create_checkout_session(self, payment: Payment, payment_method: str) -> dict:
        if payment_method.lower() == "pix":
            success_url = os.getenv("MERCADO_PAGO_SUCCESS_URL", "http://localhost:5173/success")
            cancel_url = os.getenv("MERCADO_PAGO_CANCEL_URL", "http://localhost:5173/cancel")
            session_url = create_mercadopago_checkout_preference(
                amount=payment.amount,
                currency=payment.currency,
                description=payment.description,
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {"url": session_url}
        else:
            payment_record = PaymentModel(
                amount=payment.amount,
                currency=payment.currency,
                description=payment.description,
                payment_method="stripe",
                status="pending"
            )
            payment_record.save()

            success_url = os.getenv("STRIPE_SUCCESS_URL", "http://localhost:5173/success")
            cancel_url = os.getenv("STRIPE_CANCEL_URL", "http://localhost:5173/cancel")
            amount_cents = int(payment.amount * 100)

            metadata = {"internal_payment_id": str(payment_record.id)}
            session = create_stripe_checkout_session(
                amount_cents=amount_cents,
                currency=payment.currency,
                description=payment.description,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata
            )

            payment_record.update(set__stripe_session_id=session["id"])

            return {"url": session.url}

    def update_payment_status(self, payment_id: str, status: str, updated_at=None):
        if updated_at is None:
            updated_at = datetime.datetime.utcnow()

        PaymentModel.objects(id=payment_id).update(
            set__status=status,
            set__updated_at=updated_at
        )
