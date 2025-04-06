# repositories/payment_repository.py
import mercadopago
from entities.payment import Payment
from models.payment_model import PaymentModel
import os
import json

class PaymentRepository:
    def __init__(self):
        access_token = os.getenv("ACCESS_TOKEN")
        print("DEBUG: ACCESS_TOKEN utilizado:", access_token)
        self.sdk = mercadopago.SDK(access_token)

    def create_payment(self, payment: Payment) -> PaymentModel:
        payment_data = {
            "transaction_amount": payment.transaction_amount,
            "description": payment.description,
            "payment_method_id": payment.payment_method_id,
            "payer": {"email": payment.payer_email},
        }

        # Se for pagamento com cartão, inclua token e identificação
        if payment.payment_method_id in ["credit_card", "debit_card"]:
            if not payment.token or not payment.payer_cpf:
                raise Exception("Token e CPF são obrigatórios para pagamentos com cartão.")
            payment_data["token"] = payment.token
            payment_data["payer"]["identification"] = {
                "type": "CPF",
                "number": payment.payer_cpf,
            }
        
        print("DEBUG: Dados enviados para a API Mercado Pago:")
        print(json.dumps(payment_data, indent=2, ensure_ascii=False))
        
        response = self.sdk.payment().create(payment_data)
        
        print("DEBUG: Resposta completa da API Mercado Pago:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        # Verificação de erros na resposta
        if "error" in response or "response" not in response:
            raise Exception(f"Erro ao criar pagamento: {response}")
        
        payment_info = response["response"]
        if "id" not in payment_info:
            raise Exception(f"ID do pagamento não encontrado: {payment_info}")
        
        return PaymentModel(
            id=str(payment_info["id"]),
            status=payment_info["status"],
            preference_id=str(payment_info["id"]),
            payment_url=payment_info.get("point_of_interaction", {}).get("transaction_data", {}).get("ticket_url"),
        )
