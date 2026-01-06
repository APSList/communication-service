from generated import communication_pb2_grpc, communication_pb2
import os

from customer_client import get_customer
from email_sender import send_email
from logging_config import get_logger

logger = get_logger(__name__)

CUSTOMER_SERVICE_ADDR = os.getenv("CUSTOMER_SERVICE_ADDR", "hostflow.software:443")


class CommunicationService(communication_pb2_grpc.CommunicationServiceServicer):
    def SendEmail(self, request, context):
        customer_id = getattr(request, "customer_id", None)
        property_id = getattr(request, "property_id", None)
        email_type = getattr(request, "type", None)
        payment_url = getattr(request, "payment_url", None)

        logger.info("Received SendEmail request customer_id=%s property_id=%s type=%s", customer_id, property_id, email_type)

        customer, err = get_customer(customer_id, target=CUSTOMER_SERVICE_ADDR)
        if err:
            if err == "not_found":
                message = f"Message received: {customer_id}; customer not found"
                logger.warning(message)
            else:
                message = f"Message received: {customer_id}; error fetching customer: {err}"
                logger.error(message)
            return communication_pb2.SendEmailResponse(success=False, message=message)
        elif customer is None:
            message = f"Message received: {customer_id}; customer not found"
            logger.warning(message)
            return communication_pb2.SendEmailResponse(success=False, message=message)
        else:
            c = customer
            # Construct subject/body
            if email_type == 0 or email_type == 1:
                subject = f"Payment Instructions {property_id}"
                email_body = (f"Dear {c.full_name},\n\n"
                              f"This is an automated message regarding your property with ID {property_id}.\n"
                              f"Please visit the following link to complete your payment: {payment_url}\n\n"
                              f"Best regards,\n"
                              f"The HostFlow Team")
            else:
                subject = f"Booking confirmation {property_id}"
                email_body = (f"Dear {c.full_name},\n\n"
                              f"Thank you for your booking at our property with ID {property_id}.\n"
                              f"We look forward to hosting you!\n\n"
                              f"Best regards,\n"
                              f"The HostFlow Team")

            try:
                send_email(to_email=c.email, subject=subject, body=email_body)
                logger.info("Email sent to customer id=%s email=%s", getattr(c, "id", None), getattr(c, "email", None))
            except Exception:
                logger.exception("Failed to send email for customer id=%s", getattr(c, "id", None))
                message = f"Message received: {customer_id}; failed to send email"
                return communication_pb2.SendEmailResponse(success=False, message=message)

            message = (
                f"Message received: {customer_id}; "
                f"customer id={c.id} name={c.full_name} email={c.email}"
            )
            logger.debug("SendEmail response message: %s", message)
            return communication_pb2.SendEmailResponse(success=True, message=message)
