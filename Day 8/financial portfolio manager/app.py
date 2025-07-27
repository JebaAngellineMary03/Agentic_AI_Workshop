import streamlit as st
from agents import user_proxy_agent

st.set_page_config(page_title="Financial Portfolio Manager", layout="centered")
st.title("💼 Financial Portfolio Manager")

if 'chat' not in st.session_state:
    st.session_state['chat'] = []

with st.form("portfolio_form"):
    salary = st.number_input("Current Salary (in your currency)", min_value=0, step=1000)
    portfolio = st.text_area("Describe your current investment portfolio (e.g., fixed deposits, SIPs, real estate, etc.)")
    submitted = st.form_submit_button("Analyze Portfolio")

if submitted:
    user_data = {'salary': salary, 'portfolio': portfolio}
    st.session_state['chat'] = []
    report = user_proxy_agent(user_data, st.session_state['chat'])
    st.success("Personalized Financial Report generated!")
    st.write(report)

if st.session_state['chat']:
    with st.expander("Show Agent Conversation Log"):
        for role, msg in st.session_state['chat']:
            st.markdown(f"**{role}:** {msg}") 