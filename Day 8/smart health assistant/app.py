import streamlit as st
from agents import HealthAgentOrchestrator

st.set_page_config(page_title="🤖 Smart Health AutoGen Assistant", layout="wide")
st.title("🏥 Smart Health Assistant (AutoGen Agents)")
st.markdown("A reasoning-based multi-agent health planner using Gemini AI.")

with st.form("health_form"):
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    age = st.number_input("Age", min_value=10, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    dietary = st.selectbox("Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
    submitted = st.form_submit_button("Generate Health Plan")

if submitted:
    orchestrator = HealthAgentOrchestrator()
    output = orchestrator.run(weight, height, age, gender, dietary)

    st.success("✅ User Data Collected")
    st.json(output["user"])

    st.info(f"**BMI Value:** {output['bmi']['data']['bmi']}")
    st.markdown("### 💡 BMI Reasoning")
    st.write(output['bmi']['reasoning'])
    st.markdown("### 🧠 BMI Insights")
    st.write(output['bmi']['data']['bmi_insights'])

    st.markdown("### 🍽️ Diet Plan")
    st.write(output['diet']['data']['meal_plan'])
    st.markdown("**Reasoning:**")
    st.caption(output['diet']['reasoning'])

    st.markdown("### 🏋️ Workout Plan")
    st.write(output['workout']['data']['workout_plan'])
    st.markdown("**Reasoning:**")
    st.caption(output['workout']['reasoning'])
