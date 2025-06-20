from langchain_core.tools import tool
from llms.llms import llm
from prompts.prompt_templates import final_report_prompt
import json
import re
from typing import Dict

@tool
def generate_final_report_tool(content_analysis: str, clarity_tone_analysis: str, structure_analysis: Dict) -> Dict:
    """Generate comprehensive feedback report from all agent analyses"""
    try:
        def extract_score(text: str, keywords: list[str]) -> int:
            for keyword in keywords:
                matches = re.findall(fr"{keyword}[^0-9]*?(\d+)", text, re.IGNORECASE)
                for m in matches:
                    try:
                        return int(m)
                    except:
                        continue
            return 50

        content_score = extract_score(str(content_analysis), ["structure", "relevance", "content", "score"])
        clarity_score = extract_score(str(clarity_tone_analysis), ["clarity"])
        tone_score = extract_score(str(clarity_tone_analysis), ["tone"])
        flow_score = structure_analysis.get("flow_score", 50)

        overall_score = round((content_score + clarity_score + tone_score + flow_score) / 4)

        prompt = final_report_prompt.format(
            content_analysis=content_analysis,
            clarity_analysis=clarity_tone_analysis,
            structure_analysis=json.dumps(structure_analysis, indent=2)
        )

        response = llm.invoke(prompt)
        report_text = response.content if hasattr(response, 'content') else str(response)

        return {
            "overall_score": overall_score,
            "scores": {
                "content": content_score,
                "clarity": clarity_score,
                "tone": tone_score,
                "structure_flow": flow_score
            },
            "detailed_report": report_text,
            "summary": f"Overall pitch performance: {overall_score}/100"
        }

    except Exception as e:
        return {
            "overall_score": 0,
            "scores": {"content": 0, "clarity": 0, "tone": 0, "structure_flow": 0},
            "detailed_report": f"Report generation failed: {str(e)}",
            "summary": "Analysis failed"
        }
