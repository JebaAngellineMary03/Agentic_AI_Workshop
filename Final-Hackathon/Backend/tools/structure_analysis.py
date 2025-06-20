from langchain_core.tools import tool
from llms.llms import llm
from prompts.prompt_templates import structure_prompt
import json
import re
from typing import Dict, Any

@tool
def structure_analysis_tool(transcript: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze presentation structure and flow"""
    try:
        metadata_str = ", ".join(f"{k}: {v}" for k, v in metadata.items())
        prompt = structure_prompt.format(transcript=transcript, metadata=metadata_str)
        response = llm.invoke(prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)

        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        return {
            "flow_score": 50,
            "time_balance": "Could not analyze - JSON parsing failed",
            "engagement_techniques": ["Analysis incomplete"],
            "recommendations": response_text
        }

    except Exception as e:
        return {
            "flow_score": 0,
            "time_balance": f"Error: {str(e)}",
            "engagement_techniques": ["Analysis failed"],
            "recommendations": f"Structure analysis failed: {str(e)}"
        }
