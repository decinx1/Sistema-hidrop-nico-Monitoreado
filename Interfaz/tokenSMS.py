import os
from twilio.rest import Client
from dotenv import load_dotenv
#pip install twilio
#pip install python-dotenv

load_dotenv()  # Carga las variables del archivo .env

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
service_sid = os.getenv("TWILIO_SERVICE_SID")
client = Client(account_sid, auth_token)

def enviar_codigo_verificacion(numero):
    verification = client.verify \
        .v2 \
        .services(service_sid) \
        .verifications \
        .create(to=numero, channel='sms')
    return verification.sid

def verificar_codigo(numero, codigo):
    try:
        verification_check = client.verify \
            .v2 \
            .services(service_sid) \
            .verification_checks \
            .create(to=numero, code=codigo)
        return verification_check.status == "approved"
    except Exception:
        return False