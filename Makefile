.PHONY: gen-proto run

gen-proto:
	bash scripts/generate_proto.sh

run: gen-proto
	python src/server.py