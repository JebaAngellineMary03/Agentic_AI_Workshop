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

Analyze the following pitch **transcript** and **metadata** for structural quality, engagement techniques, and effectiveness. Use the following guidelines:

**Flow Example**:
- **Introduction**: Start with a brief introduction (approx. 30 seconds) that clearly states the problem or opportunity.
- **Problem Statement**: Define the problem concisely (approx. 1 minute). Explain why the problem matters to the target audience.
- **Solution**: Present the solution (approx. 2 minutes). Clearly describe the product, service, or idea and how it solves the problem.
- **Value Proposition**: Highlight the unique value of the solution (approx. 1 minute). Why is it better than existing solutions?
- **Market Opportunity**: Demonstrate the potential market and growth (approx. 1 minute). Include relevant statistics or trends.
- **Business Model**: Describe how the solution will make money (approx. 1 minute). Explain pricing, customer acquisition, and sales strategy.
- **Call to Action**: Finish with a strong call to action (approx. 30 seconds). What do you want from your audience? Investment? Support?

**Sectional Time Example**:
- The **Problem Statement** should take about **1 minute**, as it sets up the entire pitch.
- The **Solution** section should be the **longest**, approximately **2 minutes**, since it describes the core offering.
- The **Call to Action** should be **short but impactful**, lasting around **30 seconds**.

**Storytelling Examples**:
- Use **emotional appeal**: "Imagine a world where…"
- Include **personal stories**: "I was inspired to create this solution after experiencing…"
- **Case studies**: "For example, Company X saw a 20% increase in efficiency using this solution."
- Highlight **real-life impact**: "This product has already helped over 500 businesses to..."

**Case Study Examples**:
- "Let me share an example of how this solution worked for Company X…"
- "We conducted a study with 100 users and saw a **40% improvement in performance**."
- "A similar approach was taken by Company Y, which led to **5x revenue growth** in one year."

---

**Transcript Analysis**:
Analyze the following pitch **transcript** and **metadata** to assess:
1. **Flow Score** (0-100) - How well does the pitch follow the logical structure? Is it easy to follow, or does it jump between ideas without proper transitions?
2. **Time Balance Evaluation** - How well is time allocated to each section of the pitch? Does it spend too much time on the solution and too little on the problem?
3. **Engagement Techniques Detected** - Did the presenter use effective storytelling, case studies, or other techniques to engage the audience? Include examples.
4. **Recommendations to Improve** - What can the presenter do to improve the structure, clarity, and impact of the presentation?

Respond in JSON format:
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
