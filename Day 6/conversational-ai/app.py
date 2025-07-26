import streamlit as st
from agent import agent_executor

st.set_page_config(page_title="🧠 Competitor Insight Agent", layout="wide")
st.title("🧠 Competitor Insight Agent")

st.markdown("Enter your location to generate a competitor report using real-time search and Gemini reasoning.")

location = st.text_input("Enter location (e.g., Koramangala, Bangalore):")

if st.button("Generate Report"):
    if location:
        with st.spinner("Thinking like a business strategist..."):
            try:
                prompt = f"""Generate a business report for clothing store competition in {location}.
Include:
- Top 5 competitors
- Peak customer hours
- Observed footfall patterns
- Business insights for store owners"""
                result = agent_executor.run(prompt)
                st.success("✅ Report generated!")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a location.")
