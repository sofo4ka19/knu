# Information Systems Lab

Monitoring System: PostgreSQL, Prometheus, Grafana, Loki, Tempo.

## Start

1. Copy `.env.example` to `.env` and add password.
2. `docker compose up -d`
3. Connection: `docker exec postgres psql -U admin -d shop`
