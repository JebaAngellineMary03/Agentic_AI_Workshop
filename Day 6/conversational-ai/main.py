import streamlit as st
from agents.agent_builder import build_agent

st.set_page_config(page_title="Clothing Store Agent", layout="wide")

st.markdown("""
    <style>
        .title-text {
            font-size: 2.2rem;
            font-weight: bold;
            color: #4B4BFF;
        }
        .stTextInput>div>div>input {
            font-size: 1.1rem;
        }
        .response-box {
            background-color: #f9f9f9;
            border-left: 4px solid #4B4BFF;
            padding: 1.2rem;
            border-radius: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">🛍️ Bangalore Clothing Store Market Agent</div>', unsafe_allow_html=True)

agent = build_agent()

with st.container():
    with st.form("query_form"):
        st.markdown("#### 📌 Enter your query details")
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 Location", placeholder="e.g., Koramangala")
        with col2:
            business_type = st.text_input("🏪 Business Type", "clothing store")

        task = st.selectbox("🔍 What do you want to analyze?", [
            "Search Competitors",
            "Generate Market Analysis",
            "Get Location Insights"
        ])
        submitted = st.form_submit_button("🚀 Run Agent")

if submitted:
    with st.spinner("Thinking like a market analyst 🤔..."):
        if task == "Search Competitors":
            response = agent.run(f"Search clothing competitors in {location}")
        elif task == "Generate Market Analysis":
            response = agent.run(f"Generate market analysis for a {business_type} in {location}")
        elif task == "Get Location Insights":
            response = agent.run(f"Give business insights about {location}")
        else:
            response = "❌ Unknown task selected"

    st.markdown("### 📋 Output")
    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
