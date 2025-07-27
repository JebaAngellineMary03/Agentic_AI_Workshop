import streamlit as st
from agents import user_proxy_agent
import os
import json

st.set_page_config(page_title="Bill Managing Agent", layout="centered")
st.title("🧾 Bill Managing Agent")

if 'chat' not in st.session_state:
    st.session_state['chat'] = []

with st.form("bill_form"):
    uploaded_file = st.file_uploader("Upload a bill image (jpg, png, or pdf)", type=["jpg", "jpeg", "png", "pdf"])
    submitted = st.form_submit_button("Process Bill")

if submitted and uploaded_file:
    # Save uploaded file to a temp location
    file_path = os.path.join("temp_" + uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state['chat'] = []
    summary = user_proxy_agent(file_path, st.session_state['chat'])
    st.success("Bill processed and summarized!")
    st.write(summary)
    # Try to parse JSON and visualize
    try:
        # Find the first JSON object in the summary string
        start = summary.find('{')
        end = summary.rfind('}') + 1
        if start != -1 and end != -1:
            summary_json = json.loads(summary[start:end])
            category_summary = summary_json.get('category_summary', {})
            highest = summary_json.get('highest_expenditure_category', {})
            if category_summary:
                st.subheader("Spending by Category")
                st.bar_chart(category_summary)
                if highest:
                    st.info(f"Highest Expenditure: {highest['category']} (${highest['amount']})")
    except Exception as e:
        st.warning(f"Could not parse summary for visualization: {e}")
    os.remove(file_path)

if st.session_state['chat']:
    with st.expander("Show Agent Conversation Log"):
        for role, msg in st.session_state['chat']:
            st.markdown(f"**{role}:** {msg}") 