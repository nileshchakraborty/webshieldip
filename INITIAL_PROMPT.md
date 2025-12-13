You are a senior staff engineer and solution architect. Build a complete production-ready full-stack system from scratch.

Project name
WebShield Integrity Platform

Mission
This platform measures assessment integrity using probabilistic signals derived from interaction telemetry and challenge-response anchors. It must never claim tool detection and must never infer user intent. It outputs probabilistic risk scores and deterministic policy actions with full auditability.

Critical constraints
- Do not use em dashes anywhere
- Enforcement decisions must be deterministic and rule based
- LLMs must never make enforcement or accusation decisions
- LLMs only output structured features or neutral summaries
- Auditability and explainability are mandatory
- Privacy and data minimization are mandatory
- The system must work fully offline by default

High-level architecture
This is a monorepo deployed via Docker Compose.

Primary system of record
Postgres is the only source of truth for:
- Sessions and session state
- Raw events and event history
- Derived features and anomaly scores
- Dimension scores and risk timeline
- Anchor prompts, responses, and evaluations
- Prompt templates and prompt versions
- Model call history and LLM traces
- Evidence bundles
- Reviews and appeal decisions
- Experiments and metrics
- Configuration versions and hashes

No critical data may exist only in vector DB or graph DB.

Services in Docker Compose
1) api
   - Node.js 20+, Fastify, TypeScript
   - REST API and optional SSE for live updates
2) worker
   - Python 3.11+
   - Feature extraction
   - LangGraph workflows
   - LLM calls through MCP
3) postgres
   - Primary data store
4) vector-db
   - Qdrant
5) graph-db
   - Neo4j
6) web
   - Next.js 14+, App Router, TypeScript
7) ollama
   - Local model runtime

Optional providers
- OpenAI
- Gemini

Queue
Use a Postgres-based job queue by default.
Redis may be optional but not required.

Repository structure
/
  apps/
    api/
    worker/
    web/
    sim/
  packages/
    shared/
  infra/
    docker-compose.yml
    env.example
  prompts/
    anchor_self_paraphrase_v1.txt
    anchor_constraint_flip_v1.txt
    semantic_entropy_v1.txt
    evidence_summary_v1.txt
  mappings/
    anomaly_tables.csv
    difficulty_expectations.csv
  data/
    clean/
    assisted/
    partial_assist/
  docs/
    architecture.md
    governance.md
    privacy.md
    threat_model.md
  README.md

Core domain model

Events
- question_shown
- first_input
- paste
- edit_snapshot
- submit
- focus
- visibility
- anchor_shown
- anchor_response

Derived per-question features
- silence_s
- completion_s
- paste_burst_max
- paste_chars_total
- residual_s
- optional backspace_ratio

Anomaly mapping
- Piecewise bins loaded from mappings/anomaly_tables.csv

Dimensions
- entropy
- temporal
- residual
Optional:
- semantic_entropy
- focus
- graph_pattern

Aggregation
S_total = 1 - product(1 - w_i * S_i)

Accumulation
R_t = min(1, decay * R_{t-1} + S_total_t)

Policy bands
- normal
- observe
- increase_sampling
- soft_clarification
- anchors_required
- enforce

Enforcement constraints
Enforce only when all are true:
- R_t >= enforce threshold
- anchor_failures >= 2
- anomalies span at least 2 questions

Postgres schema requirements
Implement migrations for:

- sessions
- session_events
- question_features
- dimension_scores
- risk_timeline
- anchors
- model_calls
- evidence_bundles
- reviews
- configs
- experiments
- metrics

Model_calls table must store:
- provider
- model
- prompt_version
- system_prompt
- user_prompt
- raw_response
- parsed_json
- parse_success
- latency_ms
- token_counts if available
- error fields

Vector DB scope and rules

Purpose
Qdrant is used only for RAG in reviewer-facing workflows.

Allowed uses
- Evidence summarization
- Reviewer guidance retrieval
- Anchor template rotation
- Known false positive pattern references

Forbidden uses
- Never used in scoring
- Never used in enforcement
- Never used to generate numeric features

Collections
- policy_docs
- reviewer_guidance
- anchor_templates
- known_patterns

RAG contract
RAG may only be used in the evidence_summary workflow.
It must never influence numeric scores or policy decisions.

Graph DB scope and rules

Purpose
Neo4j is used only for:
- Investigation and visualization
- Weak graph pattern signals
- Session similarity exploration

Graph model
Nodes:
- Session
- User optional
- Device hashed only
- Assessment
- Question

Edges:
- USED_DEVICE
- ANSWERED
- SIMILAR_SIGNATURE
- SHARED_DEVICE
- SHARED_NETWORK

Session signature
Computed from Postgres-derived features only.
Stored in Postgres and optionally embedded for similarity.

Graph derived feature rules
- graph_pattern_score in range 0..1
- Weight must be <= 0.10
- Graph features must never cause enforcement
- Graph features may only increase sampling or trigger anchors

Admin UI must clearly label graph data as investigative only.

MCP scope and rules

Purpose
MCP is the unified interface for all model providers.

Responsibilities
- Provider routing
- Unified prompt execution
- Structured JSON output enforcement
- Model call tracing
- Embeddings generation

Providers
- Ollama default
- OpenAI optional
- Gemini optional

Expose functions
- complete(system_prompt, user_prompt, json_schema)
- embed(texts)
- health()

All MCP calls must log to model_calls in Postgres.

LangChain and LangGraph usage

LangChain
- Embeddings
- Prompt templating
- Output parsing helpers

LangGraph
Used for deterministic workflows:
1) semantic_entropy_workflow
2) anchor_self_paraphrase_workflow
3) anchor_constraint_flip_workflow
4) evidence_summary_workflow

Each workflow must:
- Load prompt by version
- Call MCP
- Parse JSON with Pydantic
- Fallback to heuristic on failure
- Mark uncertain flag if needed
- Persist results to Postgres

LLM rules
- Output structured JSON only
- Include uncertain flag
- Never accuse or infer intent
- Never recommend enforcement

Simulation harness

Location
apps/sim

Function
- Replay JSONL sessions
- Use same configs and mappings as production
- Generate CSV outputs and evidence bundles
- Write experiment metrics to Postgres

Metrics
- Enforcement false positive proxy
- Enforcement precision
- Median time to anchor
- Median time to enforce
- Drift metrics

Frontend requirements

Admin console
- Sessions list
- Session detail view
- Risk timeline
- Feature tables
- Anchor evaluations
- Evidence viewer
- Review console
- Experiments dashboard
- Graph visualization

API endpoints
- POST /v1/sessions
- POST /v1/sessions/:id/events
- POST /v1/sessions/:id/score
- GET /v1/sessions/:id/risk
- GET /v1/sessions/:id/evidence
- POST /v1/sessions/:id/anchors/trigger
- POST /v1/reviews/:sessionId
- GET /v1/experiments/run
- GET /v1/graphs/:sessionId

Seed and demo data
- Clean session
- Assisted-like session
- Partial-assist session

Testing
Unit tests:
- anomaly lookup
- noisy-OR math
- decay accumulation
- enforcement rules
- model call logging

Integration test:
- Boot stack
- Ingest session
- Run scoring
- Retrieve evidence

Documentation
- README with offline quickstart
- architecture.md
- governance.md
- privacy.md
- threat_model.md

Final instruction
Generate the complete repository with all code, configs, Docker Compose, and docs. Ensure it runs end to end using only Ollama by default. Do not use em dashes anywhere.