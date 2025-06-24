import os
import PyPDF2
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Sidebar - API Key input
st.sidebar.title("🔑 Gemini API Key")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")

# App Title
st.title("📚 Study Assistant (LangChain + Gemini)")
st.write("Upload your course material as PDF and get a summary + quiz questions.")

# PDF Upload
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

if api_key and pdf_file:
    os.environ["GOOGLE_API_KEY"] = api_key

    # Extract text from PDF
    def extract_pdf_text(uploaded_file):
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join(page.extract_text() for page in reader.pages)

    study_material = extract_pdf_text(pdf_file)

    # Setup Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0.5
    )

    # Summarization Prompt
    summary_prompt = f"""
    You are a helpful assistant. Summarize the following study material into concise bullet points.

    Study Material:
    {study_material[:6000]}

    Summary:
    """

    with st.spinner("Generating summary..."):
        summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary = summary_response.content
        st.subheader("📌 Summary")
        st.markdown(summary)

    # Quiz Generation Prompt
    quiz_prompt = f"""
    Based on the following summary, generate 3 multiple-choice quiz questions.
    Each question should have 4 options (a-d) and clearly indicate the correct answer.

    Summary:
    {summary}

    Questions:
    """

    with st.spinner("Generating quiz questions..."):
        quiz_response = llm.invoke([HumanMessage(content=quiz_prompt)])
        quiz = quiz_response.content
        st.subheader("📝 Quiz Questions")
        st.markdown(quiz)

elif not api_key:
    st.warning("🔑 Please enter your Gemini API key in the sidebar.")
elif not pdf_file:
    st.info("📄 Upload a PDF to continue.")
