# prompts.py
from langchain_core.prompts import PromptTemplate

# Content Analysis Prompt
content_analysis_prompt = PromptTemplate.from_template("""
You are a pitch coach. Analyze the following pitch content and return:
1. Structure Score (0-100)
2. Relevance Score (0-100)
3. Strengths
4. Weaknesses
5. Suggestions to improve

Use the following context from retrieved templates as benchmark. Be critical but constructive.

Context from similar pitches: {context}

Pitch to analyze: {question}
""")

# Structure Analysis Prompt (JSON output expected)
structure_prompt = PromptTemplate.from_template("""
You are a presentation structure evaluator.

Analyze the following pitch **transcript** and **metadata** for structural quality and engagement techniques.

--- Transcript ---
{transcript}

--- Metadata ---
{metadata}

Provide the following:
1. **Flow Score** (0-100)
2. **Time Balance Evaluation**
3. **Engagement Techniques Detected**
4. **Recommendations to Improve**

Respond in JSON:
{{
  "flow_score": int,
  "time_balance": str,
  "engagement_techniques": [str],
  "recommendations": str
}}
""")

# Clarity & Tone Prompt
clarity_tone_prompt = PromptTemplate.from_template("""
Analyze the following transcript and audio features for:
1. Clarity Score (0-100)
2. Tone Score (0-100)
3. Specific feedback for both
4. Recommendations to improve

--- Transcript ---
{transcript}

--- Audio Features ---
{audio_features}
""")

# Final Report Prompt
final_report_prompt = PromptTemplate.from_template("""
Based on the following analyses, create a coaching report:

--- Content Analysis ---
{content_analysis}

--- Clarity & Tone Analysis ---
{clarity_analysis}

--- Structure Analysis ---
{structure_analysis}

Provide:
1. Executive Summary
2. Scores Breakdown
3. Strengths
4. Areas to Improve
5. Action Items
6. Suggested Practice

Be specific and actionable.
""")
