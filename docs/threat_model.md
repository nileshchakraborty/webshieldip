# Threat Model

## Adversaries
- **Cheating Users**: Attempting to use unauthorized assistance.
- **Malicious Actors**: Attempting to game the risk scoring model.

## Mitigations
- **Probabilistic Scoring**: No single signal triggers enforcement.
- **Anchors**: Challenge-response mechanism to verify understanding.
- **Rate Limiting**: Applied at API level.
