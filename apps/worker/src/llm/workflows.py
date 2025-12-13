from typing import Dict, Any, List
from .mcp import MCPClient

class Workflows:
    def __init__(self, mcp: MCPClient):
        self.mcp = mcp

    def semantic_entropy(self, snapshots: List[str]) -> Dict[str, Any]:
        """
        Analyzes consistency of edit snapshots.
        """
        if not snapshots:
            return {"entropy_score": 0.0, "uncertain": True}
            
        sys_prompt = "You are an integrity assistant. Analyze the consistency of these text variations."
        user_prompt = f"Variations: {json.dumps(snapshots)}"
        schema = {
            "type": "object",
            "properties": {
                "entropy_score": {"type": "number", "minimum": 0, "maximum": 1},
                "uncertain": {"type": "boolean"}
            }
        }
        
        try:
            return self.mcp.complete(sys_prompt, user_prompt, schema, prompt_version="semantic_entropy_v1")
        except Exception:
            return {"entropy_score": 0.5, "uncertain": True}

    def anchor_evaluation(self, challenge: str, response: str) -> Dict[str, Any]:
        """
        Evaluates a paraphrasing anchor.
        """
        sys_prompt = "You are an integrity assistant. Verify if the paraphrase captures the original meaning."
        user_prompt = f"Original: {challenge}\nParaphrase: {response}"
        schema = {
            "type": "object",
            "properties": {
                "passed": {"type": "boolean"},
                "uncertain": {"type": "boolean"},
                "explanation": {"type": "string"},
                "scores": {"type": "object"}
            }
        }
        
        try:
            return self.mcp.complete(sys_prompt, user_prompt, schema, prompt_version="anchor_eval_v1")
        except Exception:
             return {"passed": False, "uncertain": True, "explanation": "Evaluation failed"}
import json
