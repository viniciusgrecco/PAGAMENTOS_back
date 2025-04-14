import os
import stripe

# Configuração do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_checkout_session(
    amount_cents: int, 
    currency: str, 
    description: str, 
    success_url: str, 
    cancel_url: str, 
    metadata: dict = None
) -> stripe.checkout.Session:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": description},
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        payment_intent_data={"metadata": metadata},
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata
    )
    return session
