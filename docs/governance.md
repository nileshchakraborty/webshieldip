# Governance

## LLM Usage Rules
- LLMs must **NEVER** make enforcement or accusation decisions.
- LLMs only output structured features or neutral summaries.
- All model calls are logged to `model_calls` table in Postgres.

## Auditing
- Full history of events, features, and model calls is retained in Postgres.
