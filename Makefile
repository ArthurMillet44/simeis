.PHONY: all build release clean test check help manual

all: check test build manual

build:
	cargo build

release:
	cargo rustc -p simeis-server --release -- -C code-model=kernel -C codegen-units=1
ifeq ($(OS),Windows_NT)
	@echo "Skipping strip on Windows"
else
	strip target/release/simeis-server
endif

clean:
	cargo clean

test:
	cargo test

check:
	cargo check --workspace
	cargo clippy --workspace --all-targets -- -D warnings

manual:
	typst compile doc/manual.typ doc/manual.pdf

help:
	@echo "Available targets:"
	@echo "  all      - Run checks, tests, build and manual"
	@echo "  build    - Build the project in debug mode"
	@echo "  release  - Build the project in release mode"
	@echo "  clean    - Remove build artifacts"
	@echo "  test     - Run the tests"
	@echo "  check    - Check the code without building artifacts"
	@echo "  manual   - Compile the manual to PDF"
	@echo "  help     - Show this help message"