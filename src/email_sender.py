import os

import hvac
from mailersend import MailerSendClient, EmailBuilder
from logging_config import get_logger

logger = get_logger(__name__)

client = hvac.Client(
    url='HASHICORP_VAULT_ADDR',
    token='HASHICORP_VAULT_TOKEN',
    namespace='admin'
)

read_response = client.secrets.kv.read_secret_version(path='/mailer')

MAILERSEND_API_KEY = read_response['data']['data']['MAILERSEND_API_KEY']

if not MAILERSEND_API_KEY:
    logger.warning("MAILERSEND_API_KEY environment variable is not set. Email sending will fail if attempted.")

ms = MailerSendClient(api_key=MAILERSEND_API_KEY) if MAILERSEND_API_KEY else None

def send_email(to_email: str, subject: str, body: str):
    if ms is None:
        logger.error("MailerSend client not configured (no API key). Cannot send email to %s", to_email)
        return None

    email = (EmailBuilder()
             .from_email("test@test-yxj6lj96y554do2r.mlsender.net", "Hostflow")
             .to(to_email)
             .subject(subject)
             .text(body)
             .build())

    logger.info("Sending email to %s subject=%s", to_email, subject)
    try:
        response = ms.emails.send(email)
        logger.debug("MailerSend response: %s", response)
        return response
    except Exception:
        logger.exception("Failed to send email to %s", to_email)
        raise
