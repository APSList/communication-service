#!/bin/bash
set -e

PROTO_DIR=proto
OUT_DIR=src/generated

mkdir -p "$OUT_DIR"

# Generate Python gRPC code for all .proto files in proto/
for protofile in "$PROTO_DIR"/*.proto; do
    python -m grpc_tools.protoc \
        -I"$PROTO_DIR" \
        --python_out="$OUT_DIR" \
        --grpc_python_out="$OUT_DIR" \
        "$protofile"
done

# Fix imports in generated _pb2_grpc.py files to use relative imports
for file in "$OUT_DIR"/*_pb2_grpc.py; do
    [ -e "$file" ] || continue
    # Replace lines like: import foo_pb2 as foo__pb2  -> from . import foo_pb2 as foo__pb2
    sed -i '' 's@^import \(.*_pb2\) as @from . import \1 as @' "$file" 2>/dev/null || \
    sed -i 's@^import \(.*_pb2\) as @from . import \1 as @' "$file"
done