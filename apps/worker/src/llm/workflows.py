from typing import Dict, Any, List
import json
from .mcp import MCPClient

class Workflows:
    def __init__(self, mcp: MCPClient):
        self.mcp = mcp

    def semantic_entropy(self, snapshots: List[str], question: str) -> Dict[str, Any]:
        """
        Analyzes consistency of edit snapshots to detect cosmetic vs reasoning changes.
        """
        if not snapshots:
            return {"entropy_score": 0.0, "uncertain": True}
        
        # Flatten snapshots for prompt
        drafts_text = "\n".join([f"D{i}:\n{s}" for i, s in enumerate(snapshots)])
            
        sys_prompt = (
            "You are a feature extractor. You must not judge intent, accuse a user, or mention cheating or tools. "
            "You must output only valid JSON. You must be conservative and prefer 'uncertain' over strong claims."
        )
        user_prompt = (
            f"Question:\n{question}\n\n"
            f"Drafts (chronological):\n{drafts_text}\n\n"
            "Task: Compare the drafts and produce semantic progression features."
        )
        
        schema = {
            "type": "object",
            "properties": {
                "semantic_change_total": {"type": "number", "minimum": 0, "maximum": 1},
                "semantic_change_directionality": {"type": "number", "minimum": 0, "maximum": 1},
                "cosmetic_edit_ratio": {"type": "number", "minimum": 0, "maximum": 1},
                "reasoning_added_ratio": {"type": "number", "minimum": 0, "maximum": 1},
                "early_completeness_score": {"type": "number", "minimum": 0, "maximum": 1},
                "notes": {"type": "array", "items": {"type": "string"}},
                "uncertain": {"type": "boolean"}
            },
            "required": ["semantic_change_total", "cosmetic_edit_ratio"]
        }
        
        try:
            return self.mcp.complete(sys_prompt, user_prompt, schema, prompt_version="semantic_entropy_v2")
        except Exception:
            return {"semantic_change_total": 0.5, "uncertain": True}

    def anchor_self_reference(self, user_answer: str, anchor_prompt: str, anchor_response: str) -> Dict[str, Any]:
        """
        Evaluates a self-referential paraphrase anchor.
        """
        sys_prompt = "You are a feature extractor. Do not judge intent. Do not accuse. Output only valid JSON."
        user_prompt = (
            f"User answer:\n{user_answer}\n\n"
            f"Anchor prompt:\n{anchor_prompt}\n\n"
            f"Anchor response:\n{anchor_response}\n\n"
            "Task: Assess alignment of anchor_response with user_answer."
        )
        
        schema = {
            "type": "object",
            "properties": {
                "alignment_score": {"type": "number", "minimum": 0, "maximum": 1},
                "specificity_score": {"type": "number", "minimum": 0, "maximum": 1},
                "genericness_score": {"type": "number", "minimum": 0, "maximum": 1},
                "contradiction_score": {"type": "number", "minimum": 0, "maximum": 1},
                "passed": {"type": "boolean"},
                "uncertain": {"type": "boolean"}
            }
        }
        
        try:
            return self.mcp.complete(sys_prompt, user_prompt, schema, prompt_version="anchor_self_ref_v1")
        except Exception:
            return {"passed": False, "uncertain": True}

    def anchor_constraint_flip(self, question: str, user_answer: str, flip_condition: str, flip_response: str) -> Dict[str, Any]:
        """
        Evaluates a constraint flip anchor.
        """
        sys_prompt = "You are a feature extractor. Do not judge intent. Output only valid JSON."
        user_prompt = (
            f"Question:\n{question}\n\n"
            f"User answer:\n{user_answer}\n\n"
            f"Constraint change:\n{flip_condition}\n\n"
            f"User response to constraint:\n{flip_response}\n\n"
            "Task: Evaluate whether the response correctly adapts the original approach under the constraint change."
        )
        
        schema = {
            "type": "object",
            "properties": {
                "adaptation_correctness": {"type": "number", "minimum": 0, "maximum": 1},
                "consistency_with_original": {"type": "number", "minimum": 0, "maximum": 1},
                "handwaving_score": {"type": "number", "minimum": 0, "maximum": 1},
                "passed": {"type": "boolean"},
                "uncertain": {"type": "boolean"}
            }
        }
        
        try:
            return self.mcp.complete(sys_prompt, user_prompt, schema, prompt_version="anchor_constraint_flip_v1")
        except Exception:
            return {"passed": False, "uncertain": True}
