import os
import streamlit as st
from workflows.eda_workflow import run_workflow
import pandas as pd

st.set_page_config(page_title="Multi-Agent EDA System", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🤖 Multi-Agent EDA System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a CSV/Excel file or use the sample data to automatically clean, analyze, visualize, and critique the data using a multi-agent architecture.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Upload your CSV or Excel file", type=["csv", "xls", "xlsx"])

os.makedirs("data", exist_ok=True)
if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
    save_path = f"data/data{file_ext}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
else:
    # Generate a sample dataset
    save_path = "data/sample.csv"
    df = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024]*4,
        'Industry': ['A', 'B', 'C', 'D']*5,
        'Income': [100, 120, 130, 140, 150, 200, 210, 220, 230, 240, 300, 310, 320, 330, 340, 400, 410, 420, 430, 440],
        'Expenditure': [80, 90, 100, 110, 120, 160, 170, 180, 190, 200, 240, 250, 260, 270, 280, 320, 330, 340, 350, 360],
        'Profit': [20, 30, 30, 30, 30, 40, 40, 40, 40, 40, 60, 60, 60, 60, 60, 80, 80, 80, 80, 80]
    })
    df.to_csv(save_path, index=False)

with st.spinner("⏳ Running multi-agent workflow..."):
    report, feedback, validation, image_paths = run_workflow(save_path)

st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📘 Final Report")
    st.markdown(report, unsafe_allow_html=True)

with col2:
    st.subheader("🖼️ Visualizations")
    for img in image_paths:
        st.image(img, use_container_width=True)
st.markdown("---")

with st.container():
    st.subheader("🧠 Critic Feedback")
    st.code(feedback, language="markdown")

with st.container():
    st.subheader("✅ Report Validation")
    st.success(validation) 