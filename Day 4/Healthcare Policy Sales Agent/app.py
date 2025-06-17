# app.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from policy_data import policies, add_ons

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Healthcare Policy Advisor", page_icon="🏥", layout="centered")
st.title("🏥 Healthcare Policy Advisor")
st.markdown("Let me recommend the best **HealthSecure** insurance policy based on your needs.")

with st.form("policy_form"):
    age = st.number_input("Your age", min_value=0, max_value=120)
    coverage_type = st.selectbox("Coverage type", ["individual", "family"])
    dependents = st.number_input("Number of dependents", min_value=0, max_value=10)
    needs = st.multiselect(
        "Special requirements?",
        ["dental", "vision", "maternity", "mental health", "wellness", "travel"]
    )
    submit = st.form_submit_button("Get Recommendation")

def build_prompt(age, coverage_type, dependents, needs):
    needs_text = ", ".join(needs) if needs else "none"
    return f"""
You are a healthcare insurance advisor.

Based on the following user input, recommend the best policy from HealthSecure Insurance Ltd:

- Age: {age}
- Coverage Type: {coverage_type}
- Dependents: {dependents}
- Special Requirements: {needs_text}

Match policies using:
- age eligibility
- family type
- special features (like maternity, dental, travel, etc.)

Also suggest add-ons only if not already included in the chosen plan.

Give the output in the following format:
• Recommended Plan: [Name]
• Why this fits: [Explanation]
• Monthly Premium: [$]
• Suggested Add-Ons (if any): [List or None]
"""

if submit:
    with st.spinner("Consulting HealthSecure policies..."):
        prompt = build_prompt(age, coverage_type, dependents, needs)
        response = model.generate_content(prompt)
        st.success("✅ Here is your personalized recommendation:")
        st.markdown(response.text)
