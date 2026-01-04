from generated import communication_pb2_grpc, communication_pb2
import grpc
import os

from customer_client import get_customer

CUSTOMER_SERVICE_ADDR = os.getenv("CUSTOMER_SERVICE_ADDR", "hostflow.software:443")

class CommunicationService(communication_pb2_grpc.CommunicationServiceServicer):
    def SendMessage(self, request, context):
        print("CommunicationService.SendMessage")
        customer_id = getattr(request, "customer_id", None)

        try:
            resp = get_customer(customer_id, target=CUSTOMER_SERVICE_ADDR)
            if resp and resp.customer:
                c = resp.customer
                message = (
                    f"Message received: {customer_id}; "
                    f"customer id={c.id} name={c.full_name} email={c.email}"
                )
            else:
                message = f"Message received: {customer_id}; customer not found"
        except grpc.RpcError as e:
            code = e.code() if hasattr(e, "code") else None
            details = e.details() if hasattr(e, "details") else str(e)
            message = f"Message received: {customer_id}; error fetching customer: {code}: {details}"
        except Exception as e:
            message = f"Message received: {customer_id}; unexpected error: {e}"

        return communication_pb2.MessageReply(message=message)
