#!/bin/bash
set -e

PROTO_DIR=proto
OUT_DIR=src/generated

mkdir -p "$OUT_DIR"

python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUT_DIR" \
    --grpc_python_out="$OUT_DIR" \
    "$PROTO_DIR"/communication.proto

for file in "$OUT_DIR"/*_pb2_grpc.py; do
    [ -e "$file" ] || continue
    sed -i '' 's@^import communication_pb2 as @from . import communication_pb2 as @' "$file" 2>/dev/null || \
    sed -i 's@^import communication_pb2 as @from . import communication_pb2 as @' "$file"
done