# WebShield Integrity & Privacy Policy

## 1. Core Principles
*   **Privacy-First Telemetry**: We do not capture full screen video, audio, or invasive device fingerprints. We collect only necessary behavioral metadata (keystroke dynamics, focus events, edit snapshots).
*   **No Automated Bans**: All high-stakes decisions (e.g., test invalidation) require human review or are subject to a robust appeals process.
*   **Transparency**: Users are notified when monitoring is active. Risk bands are not secret, though specific triggering thresholds may be obscured to prevent gaming.
*   **Accommodation**: Users with verified needs (e.g., screen readers, extend time) are assigned alternative weighing profiles to prevent false positives.

## 2. Data Retention
*   **Raw Telemetry**: Retained for 24 hours (or duration of exam session + 1 hour).
*   **Risk Scores & Flags**: Retained for 90 days.
*   **Anonymized Statistics**: Retained indefinitely for model training.

## 3. Enforcement Ladder
| Risk Band | Description | Actions |
| :--- | :--- | :--- |
| **Trusted** | Clear evidence of honest behavior. | No friction. |
| **Observe** | Minor anomalies or insufficient data. | Silent logging. Sampling for review. |
| **Anchors Required** | Multiple behavioral flags (e.g., speed, paste). | Trigger cognitive verification (Anchors). |
| **Enforce** | Corroborated evidence (Flags + Anchor Failures). | Invalidate session. Flag for manual review. |

## 4. Appeals Process
1.  **Notification**: Users are informed of the *reason* for flagging (e.g., "Inconsistent typing patterns detected").
2.  **Request Review**: User can request a manual review within 7 days.
3.  **Human Audit**: A trained reviewer examines the "Evidence Bundle" (edit replay, session graph).
4.  **Outcome**: Decision overturned (score cleared) or upheld.
