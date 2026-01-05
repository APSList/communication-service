import grpc
from generated import customer_pb2, customer_pb2_grpc
from urllib.parse import urlparse

DEFAULT_TARGET = "hostflow.software:443"

def _make_channel(target: str):
    parsed = urlparse(target if '://' in target else f"//{target}", scheme='')
    hostport = parsed.netloc or parsed.path
    if hostport.endswith(":443"):
        creds = grpc.ssl_channel_credentials()
        return grpc.secure_channel(hostport, creds)
    return grpc.insecure_channel(hostport)


def get_customer(customer_id: int, target: str = DEFAULT_TARGET, timeout: float = 5.0):
    channel = _make_channel(target)
    with channel:
        stub = customer_pb2_grpc.CustomerServiceStub(channel)
        req = customer_pb2.GetCustomerRequest(id=customer_id)
        return stub.GetCustomer(req, timeout=timeout)
