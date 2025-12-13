# Architecture

WebShield is a monorepo deployed via Docker Compose.

## Services
- **API**: Node.js/Fastify. Primary entry point for events.
- **Worker**: Python. Extracts features, runs LangGraph workflows.
- **Web**: Next.js. Admin dashboard.
- **Postgres**: Primary system of record.
- **Qdrant**: Vector DB for RAG (Reviewer guidance only).
- **Neo4j**: Graph DB for investigation.
- **Ollama**: Local LLM inference.

## Data Flow
1. Events -> API -> Postgres.
2. Worker -> Polls Events -> Extracts Features -> Postgres.
3. Worker -> Risk Analysis -> Postgres.
