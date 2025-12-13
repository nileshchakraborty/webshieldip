# WebShield Integrity Platform

WebShield is a production-ready full-stack system for measuring assessment integrity using probabilistic signals and challenge-response anchors.

## Quickstart (Offline)

1.  **Prerequisites**: Docker Desktop, Node.js 20+, Python 3.11+.
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Start Services**:
    ```bash
    cd infra
    docker compose up -d
    ```
    This will start API (3001), Web (3000), Worker, Postgres, Qdrant, Neo4j, and Ollama.

4.  **Run Simulation**:
    ```bash
    # In another terminal
    python apps/sim/src/runner.py apps/sim/data/sample_session.jsonl
    ```

## Architecture
See [docs/architecture.md](docs/architecture.md) for details.

## Governance
See [docs/governance.md](docs/governance.md).

## Privacy
See [docs/privacy.md](docs/privacy.md).
