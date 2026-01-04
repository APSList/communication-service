import argparse
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


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Minimal gRPC client for CustomerService.GetCustomer")
    p.add_argument("--id", type=int, required=True, help="Customer id to fetch")
    p.add_argument("--target", default=DEFAULT_TARGET, help="gRPC server address (host:port)")
    p.add_argument("--timeout", type=float, default=5.0, help="RPC timeout seconds")
    args = p.parse_args()

    try:
        resp = get_customer(args.id, args.target, timeout=args.timeout)
    except grpc.RpcError as e:
        code = e.code() if hasattr(e, "code") else None
        details = e.details() if hasattr(e, "details") else str(e)
        print(f"RPC error: {code}: {details}")
    else:
        if resp and resp.customer:
            c = resp.customer
            print(f"Customer: id={c.id} name={c.full_name} email={c.email} created_at={c.created_at}")
        else:
            print("No customer returned")

