import grpc
from concurrent import futures
from generated import communication_pb2_grpc
from services import CommunicationService
from grpc_reflection.v1alpha import reflection
from logging_config import get_logger
import threading
import http.server
import socketserver
import os

logger = get_logger(__name__)

class _HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        logger.debug("HealthHandler: %s - %s", self.address_string(), format % args)

def _start_health_server(port: int):
    try:
        with socketserver.TCPServer(("0.0.0.0", port), _HealthHandler) as httpd:
            logger.info("Health HTTP endpoint running on port %d", port)
            httpd.serve_forever()
    except OSError:
        logger.exception("Failed to start health HTTP server on port %d", port)
    except Exception:
        logger.exception("Health HTTP server crashed")

def serve():
    health_port = int(os.getenv("HEALTH_PORT", "8000"))
    try:
        t = threading.Thread(target=_start_health_server, args=(health_port,), daemon=True)
        t.start()
    except Exception:
        logger.exception("Failed to start health thread")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_CommunicationServiceServicer_to_server(CommunicationService(), server)

    SERVICE_NAMES = (
        communication_pb2_grpc.CommunicationServiceServicer.__name__,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    try:
        server.start()
        logger.info("gRPC server running on port 50051 with reflection")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("gRPC server shutting down (KeyboardInterrupt)")
        server.stop(0)
    except Exception:
        logger.exception("gRPC server failed")

if __name__ == "__main__":
    serve()
