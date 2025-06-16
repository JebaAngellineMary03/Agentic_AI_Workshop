import streamlit as st
import tempfile
from utils.metadata import extract_metadata_and_text, split_sections,clean_section_titles
from utils.citation import get_citation_count
from utils.gemini_analysis import analyze_section_with_gemini
from utils.rag_similarity import fetch_similar_papers, reconstruct_openalex_abstract, generate_comparison
import pandas as pd

st.set_page_config(page_title="📄 Research Paper Authorship Checker", layout="wide")
st.title("📄 Research Paper Authorship Checker with RAG Similarity")

uploaded_file = st.file_uploader("📤 Upload a Research Paper (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("🔍 Extracting metadata..."):
        data = extract_metadata_and_text(tmp_path)

    st.subheader("📌 Metadata")
    col1, col2 = st.columns(2)
    col1.markdown(f"**📄 Title:** {data['title']}")
    col2.markdown(f"**✍️ Authors:** {data['authors']}")

    with st.spinner("📈 Fetching citation count..."):
        count = get_citation_count(data["title"])
    st.markdown(f"**📊 Citation Count:** `{count}`")

    st.subheader("📚 Section-wise AI Authorship Verdict")
    with st.spinner("📖 Analyzing sections with Gemini..."):
        sections = split_sections(data["full_text"])
        sections = clean_section_titles(sections)

        if not sections:
            st.warning("⚠️ No clear section headings found.")
        else:
            verdicts = []
            for sec_title, sec_text in sections.items():
                verdict = analyze_section_with_gemini(sec_title, sec_text)
                short_verdict = "✅ Human-written" if "Human" in verdict else "❌ AI-generated"
                verdicts.append({"Section": sec_title, "Verdict": short_verdict})

            df = pd.DataFrame(verdicts)
            df.index = [f"{i+1}" for i in range(len(df))]
            st.dataframe(df.style.set_properties(**{'text-align': 'left'}), use_container_width=True, height=450)

    st.subheader("🔍 RAG-Based Abstract Similarity Check")
    abstract = data["abstract"]
    if not abstract:
        st.warning("⚠️ Abstract not found for similarity comparison.")
    else:
        with st.spinner("🌐 Fetching similar papers from OpenAlex..."):
            similar_papers = fetch_similar_papers(data["title"])
            similar_abstracts = "\n\n".join([
                reconstruct_openalex_abstract(p.get("abstract_inverted_index", {})) for p in similar_papers
            ])

        with st.spinner("🧠 Comparing with Gemini..."):
            rag_result = generate_comparison(abstract, similar_abstracts)
            st.markdown("### 📝 Similarity Report")
            st.info(rag_result)
