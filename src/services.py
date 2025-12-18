from generated import communications_pb2_grpc, communications_pb2
import grpc

class HelloWorld(communications_pb2_grpc.HelloWorldServicer):
    async def SayHello(self, request, context):
        return communications_pb2.HelloReply(message=f"Hello, {request.name}!")