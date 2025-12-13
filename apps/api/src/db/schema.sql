-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    assessment_id TEXT,
    user_hash TEXT,
    device_hash TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Event History
CREATE TABLE IF NOT EXISTS event_history (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    question_id TEXT,
    event_type TEXT NOT NULL,
    payload JSONB,
    ts_ms BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_events_session ON event_history(session_id);
CREATE INDEX idx_events_ts ON event_history(ts_ms);

-- Question Features
CREATE TABLE IF NOT EXISTS question_features (
    session_id TEXT REFERENCES sessions(id),
    question_id TEXT NOT NULL,
    question_index INT NOT NULL,
    silence_s FLOAT,
    completion_s FLOAT,
    paste_burst_max INT,
    paste_chars_total INT,
    residual_s FLOAT,
    backspace_ratio FLOAT,
    PRIMARY KEY (session_id, question_id)
);

-- Dimension Scores
CREATE TABLE IF NOT EXISTS dimension_scores (
    session_id TEXT REFERENCES sessions(id),
    question_id TEXT NOT NULL,
    dimension TEXT NOT NULL,
    score FLOAT NOT NULL,
    scoring_version TEXT,
    PRIMARY KEY (session_id, question_id, dimension)
);

-- Risk Timeline
CREATE TABLE IF NOT EXISTS risk_timeline (
    session_id TEXT REFERENCES sessions(id),
    question_index INT NOT NULL,
    s_total FLOAT NOT NULL,
    r_t FLOAT NOT NULL,
    policy_band TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id, question_index)
);

-- Anchors
CREATE TABLE IF NOT EXISTS anchors (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    question_id TEXT,
    anchor_type TEXT NOT NULL,
    trigger_reason TEXT,
    prompt_version TEXT,
    challenge_text TEXT,
    response_text TEXT,
    evaluation JSONB,
    passed BOOLEAN,
    uncertain BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Model Calls (Audit Log)
CREATE TABLE IF NOT EXISTS model_calls (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_version TEXT,
    system_prompt TEXT,
    user_prompt TEXT,
    raw_response TEXT,
    parsed_json JSONB,
    parse_success BOOLEAN,
    latency_ms INT,
    token_counts JSONB,
    error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_model_calls_session ON model_calls((parsed_json->>'session_id'));

-- Evidence Bundles
CREATE TABLE IF NOT EXISTS evidence_bundles (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    config_hash TEXT,
    scoring_version TEXT,
    content JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
