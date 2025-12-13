export type EventType =
    | 'question_shown'
    | 'first_input'
    | 'paste'
    | 'edit_snapshot'
    | 'submit'
    | 'focus'
    | 'visibility'
    | 'anchor_shown'
    | 'anchor_response';

export type PolicyBand =
    | 'normal'
    | 'observe'
    | 'increase_sampling'
    | 'soft_clarification'
    | 'anchors_required'
    | 'enforce';

export interface Session {
    id: string;
    assessment_id?: string;
    user_hash?: string;
    device_hash: string;
    status: 'active' | 'completed' | 'flagged';
    created_at: number; // Unix timestamp ms
}

export interface Event {
    id: string;
    session_id: string;
    question_id: string;
    event_type: EventType;
    payload: Record<string, any>;
    ts_ms: number; // Client timestamp
    server_received_ts?: number;
}

export interface QuestionFeatures {
    session_id: string;
    question_id: string;
    question_index: number;
    silence_s: number;
    completion_s: number;
    paste_burst_max: number;
    paste_chars_total: number;
    residual_s: number;
    backspace_ratio: number;
}

export interface DimensionScore {
    session_id: string;
    question_id: string;
    dimension: string;
    score: number;
    scoring_version: string;
}

export interface RiskTimeline {
    session_id: string;
    question_index: number;
    s_total: number;
    r_t: number;
    policy_band: PolicyBand;
}

export interface Anchor {
    session_id: string;
    question_id: string;
    anchor_type: string;
    trigger_reason: string;
    prompt_version: string;
    challenge_text: string;
    response_text?: string;
    evaluation?: {
        passed: boolean;
        uncertain: boolean;
        scores: Record<string, number>;
        explanation: string;
    };
    passed?: boolean;
    uncertain?: boolean;
}

export interface ModelCall {
    id: string;
    provider: string;
    model: string;
    prompt_version: string;
    system_prompt: string;
    user_prompt: string;
    raw_response: string;
    parsed_json: Record<string, any>;
    parse_success: boolean;
    latency_ms: number;
    token_counts?: { input: number; output: number };
    error?: string;
    created_at: number;
}

export interface EvidenceBundle {
    session_id: string;
    config_hash: string;
    scoring_version: string;
    content: {
        summary: string;
        events_snapshot: Event[];
        features_snapshot: QuestionFeatures[];
    };
    created_at: number;
}
