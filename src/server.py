import grpc
from concurrent import futures
from generated import communication_pb2_grpc
from services import CommunicationService
from grpc_reflection.v1alpha import reflection

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_CommunicationServiceServicer_to_server(CommunicationService(), server)

    SERVICE_NAMES = (
        communication_pb2_grpc.CommunicationServiceServicer.__name__,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051 with reflection")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
