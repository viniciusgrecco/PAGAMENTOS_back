import os
import requests

def create_mercadopago_checkout_preference(amount: float, currency: str, description: str, success_url: str, cancel_url: str) -> str:
    access_token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
    if not access_token:
        raise Exception("Mercado Pago access token não configurado.")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "items": [{
            "title": description,
            "quantity": 1,
            "unit_price": amount
        }],
        "back_urls": {
            "success": success_url,
            "failure": cancel_url,
            "pending": cancel_url
        },
        "auto_return": "approved"  
    }

    response = requests.post("https://api.mercadopago.com/checkout/preferences", json=body, headers=headers)
    data = response.json()
    if response.status_code not in (200, 201):
        raise Exception(f"Erro ao criar a preference no Mercado Pago: {data}")
    
    return data.get("init_point")
