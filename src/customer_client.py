import grpc
from generated import customer_pb2, customer_pb2_grpc
from urllib.parse import urlparse
from typing import Optional,  Tuple

DEFAULT_TARGET = "hostflow.software:443"

def _make_channel(target: str):
    parsed = urlparse(target if '://' in target else f"//{target}", scheme='')
    hostport = parsed.netloc or parsed.path
    if hostport.endswith(":443"):
        creds = grpc.ssl_channel_credentials()
        return grpc.secure_channel(hostport, creds)
    return grpc.insecure_channel(hostport)


def get_customer_unsafe(customer_id: int, target: str = DEFAULT_TARGET, timeout: float = 5.0) -> customer_pb2.CustomerResponse:
    channel = _make_channel(target)
    with channel:
        stub = customer_pb2_grpc.CustomerServiceStub(channel)
        req = customer_pb2.GetCustomerRequest(id=customer_id)
        return stub.GetCustomer(req, timeout=timeout)


def get_customer(customer_id: int, target: str = DEFAULT_TARGET, timeout: float = 5.0) -> Tuple[Optional[customer_pb2.Customer], Optional[str]]:
    try:
        resp = get_customer_unsafe(customer_id, target=target, timeout=timeout)
        if resp is None:
            return None, "not_found"
        customer = resp.customer if hasattr(resp, "customer") else None
        if customer is None:
            return None, "not_found"
        is_populated = bool(
            getattr(customer, "id", 0) or getattr(customer, "full_name", "") or getattr(customer, "email", "") or getattr(customer, "created_at", "")
        )
        if not is_populated:
            return None, "not_found"
        return customer, None
    except grpc.RpcError as e:
        code = e.code() if hasattr(e, "code") else None
        details = e.details() if hasattr(e, "details") else str(e)
        return None, f"{code}: {details}"
    except Exception as e:
        return None, f"error: {e}"
