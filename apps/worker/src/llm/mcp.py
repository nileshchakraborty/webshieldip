import os
import json
import time
import requests
import uuid
from typing import Dict, Any, Optional

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
DB_URL = os.getenv("DATABASE_URL")

class MCPClient:
    """
    Model Context Protocol Client.
    Handles routing, audit logging, and structured output enforcement.
    """
    def __init__(self, db_conn):
        self.db = db_conn

    def complete(self, 
                 system_prompt: str, 
                 user_prompt: str, 
                 json_schema: Dict[str, Any], 
                 model: str = "llama3",
                 prompt_version: str = "v1",
                 provider: str = "ollama") -> Dict[str, Any]:
        
        call_id = str(uuid.uuid4())
        start_time = time.time()
        
        # 1. Prepare Request
        # Only implementing Ollama for offline constraint
        url = f"{OLLAMA_URL}/api/generate"
        
        prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nOutput strictly valid JSON matching: {json.dumps(json_schema)}"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }
        
        raw_resp = ""
        parsed = {}
        success = False
        error_msg = None
        
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                raw_resp = resp.json().get('response', '')
                try:
                    parsed = json.loads(raw_resp)
                    # Basic schema validation could happen here
                    success = True
                except json.JSONDecodeError:
                    error_msg = "JSON Parse Failed"
            else:
                error_msg = f"HTTP {resp.status_code}: {resp.text}"
                
        except Exception as e:
            error_msg = str(e)
            
        latency_ms = int((time.time() - start_time) * 1000)
        
        # 2. Audit Log (Async or blocking? Blocking for safety)
        self._log_call(call_id, provider, model, prompt_version, system_prompt, user_prompt, 
                       raw_resp, parsed, success, latency_ms, error_msg)
        
        if not success:
            raise Exception(f"MCP Call Failed: {error_msg}")
            
        return parsed

    def _log_call(self, id, provider, model, p_ver, sys_p, usr_p, raw, parsed, success, lat, err):
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO model_calls 
                (id, provider, model, prompt_version, system_prompt, user_prompt, 
                 raw_response, parsed_json, parse_success, latency_ms, error, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (id, provider, model, p_ver, sys_p, usr_p, raw, json.dumps(parsed), success, lat, err))
            self.db.commit()

    def embed(self, texts: list[str]) -> list[list[float]]:
        # Placeholder for embedding implementation
        return [[0.0] * 768 for _ in texts]
