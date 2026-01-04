from generated import communication_pb2_grpc, communication_pb2
import grpc
import os

CUSTOMER_SERVICE_ADDR = os.getenv("CUSTOMER_SERVICE_ADDR", "hostflow.software:443")

class CommunicationService(communication_pb2_grpc.CommunicationServiceServicer):
    def SendMessage(self, request, context):
        print("CommunicationService.SendMessage")
        message = f"Message received: {request.customer_id}"

        return communication_pb2.MessageReply(message=message)
