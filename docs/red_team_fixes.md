# Red Team Hardening Report

## Summary
This document details the hardening measures implemented in response to the Red Team review. The focus was on defensive robustness, auditability, and preventing adversarial bypasses.

## 1. Scoring Robustness
- **Issue**: Single dimension spikes could trigger enforcement too easily (False Positives).
- **Fix**: Implemented `calculate_risk_score` with hard caps per dimension.
- **Rule**: "Two-Signal Requirement" ensures `anchors_required` band (0.85+) is only reached if at least 2 dimensions exceed 0.6 threshold.

## 2. Anchor Policy
- **Issue**: Anchors were vulnerable to spamming or ambiguity.
- **Fix**: 
    - **Rate Limits**: Max 1 anchor per 2 questions, 90s cooldown, max 3 per session.
    - **Uncertainty**: LLM uncertainty now explicitly maps to `non-failure` status to prevent false positives during model degradation.

## 3. LLM Security
- **Issue**: Prompt injection and potential for parsing failures to crash worker.
- **Fix**:
    - **Input Wrapping**: User content is wrapped in triple quotes with trusted instructions to ignore commands within.
    - **Strict JSON**: Extra keys are stripped, types are enforced.
    - **Safe Fallback**: Parse failures return a valid JSON object with `uncertain: true`, maintaining system stability without enforcing.

## 4. Deterministic Replay
- **Issue**: Race conditions in event ingestion led to non-deterministic scores.
- **Fix**: 
    - `sequencing.py`: Events are deduplicated and sorted by `ts_ms` + `id` (tie-break).
    - Question indices are inferred deterministically from sorted entry times.

## 5. Evidence Governance
- **Issue**: Enforcement could happen with incomplete audit trails.
- **Fix**: `check_completeness` gate ensures `config_hash`, `scoring_version`, and `model_call_ids` are present before `can_enforce` returns True.

## 6. Store Guardrails
- **Issue**: Risk of leaking session PII into vector stores.
- **Fix**: `QdrantGuardrail` enforces allowlist for collections (`policy_docs` etc.) and scans payloads for `session_id` to block accidental writes.
