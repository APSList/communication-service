FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/ ./proto
COPY src/ ./src
COPY scripts/ ./scripts

# Generate gRPC code
RUN bash scripts/generate_proto.sh

EXPOSE 50051

CMD ["python", "src/server.py"]