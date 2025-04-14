from mongoengine import Document, StringField, FloatField, DateTimeField
import datetime

class PaymentModel(Document):
    amount = FloatField(required=True)
    currency = StringField(default="brl")
    description = StringField(default="Doação")
    payment_method = StringField(required=True)  
    stripe_session_id = StringField()           
    status = StringField(default="pending")      
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
