# app.py

import streamlit as st
from src.query_engine import query_rag


st.set_page_config(page_title="RAG QA on AI Papers", layout="centered")

# -------------------- Styling --------------------
st.markdown("""
    <style>
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 1.2rem;
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .chunk-box {
            border: 1px solid #e6e6e6;
            padding: 1rem;
            border-radius: 12px;
            background-color: #f9f9f9;
            margin-bottom: 1rem;
        }
        .chunk-source {
            font-weight: bold;
            margin-bottom: 0.3rem;
            color: #333;
        }
        .answer-box {
            background-color: #f0f8ff;
            padding: 1.2rem;
            border-left: 6px solid #4a90e2;
            border-radius: 8px;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-size: 1.1rem;
            padding: 10px;
            background-color: #4a90e2;
            color: white;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown('<div class="title">🧠 AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions and get answers from AI research papers</div>', unsafe_allow_html=True)

# -------------------- Input --------------------
question = st.text_input("💬 Enter your question:", placeholder="e.g., What are the main components of a RAG model?")

# -------------------- Action Button --------------------
if st.button("🔍 Get Answer") and question.strip():
    with st.spinner("🔄 Thinking... Generating your answer..."):
        result = query_rag(question)

        # -------------------- Answer Display --------------------
        st.markdown("### 💡 Answer")
        st.markdown(f"<div class='answer-box'>{result['answer']}</div>", unsafe_allow_html=True)

        # -------------------- Source Display --------------------


