FROM rust:1.88-bookworm AS builder

WORKDIR /app

COPY . .

RUN cargo build --release -p simeis-server --no-default-features --features tokio

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl

WORKDIR /app

COPY --from=builder /app/target/release/simeis-server .

EXPOSE 8080
CMD ["./simeis-server"]

HEALTHCHECK --interval=30s --timeout=30s --retries=3 CMD curl --fail http://localhost:8080/ping || exit 1


