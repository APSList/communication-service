import asyncio
from grpc import aio
from generated import communications_pb2_grpc
from services import HelloWorld

async def serve():
    server = aio.server()

    # Register the service implementation
    communications_pb2_grpc.add_HelloWorldServicer_to_server(HelloWorld(), server)


    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f"Starting gRPC server with reflection on {listen_addr}")

    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
