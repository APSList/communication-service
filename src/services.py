from generated import communication_pb2_grpc, communication_pb2
import grpc
import os

from customer_client import get_customer
from email_sender import send_email

CUSTOMER_SERVICE_ADDR = os.getenv("CUSTOMER_SERVICE_ADDR", "hostflow.software:443")


class CommunicationService(communication_pb2_grpc.CommunicationServiceServicer):
    def SendEmail(self, request, context):
        print("CommunicationService.SendMessage")
        customer_id = getattr(request, "customer_id", None)
        property_id = getattr(request, "property_id", None)
        email_type = getattr(request, "type", None)
        payment_url = getattr(request, "payment_url", None)

        customer, err = get_customer(customer_id, target=CUSTOMER_SERVICE_ADDR)
        print(customer)
        if err:
            if err == "not_found":
                message = f"Message received: {customer_id}; customer not found"
            else:
                message = f"Message received: {customer_id}; error fetching customer: {err}"
            return communication_pb2.SendEmailResponse(success=False, message=message)
        elif customer is None:
            message = f"Message received: {customer_id}; customer not found"
            return communication_pb2.SendEmailResponse(success=False, message=message)
        else:
            c = customer
            print(email_type)
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

            send_email(to_email=c.email, subject=subject, body=email_body)

            message = (
                f"Message received: {customer_id}; "
                f"customer id={c.id} name={c.full_name} email={c.email}"
            )
            return communication_pb2.SendEmailResponse(success=True, message=message)
