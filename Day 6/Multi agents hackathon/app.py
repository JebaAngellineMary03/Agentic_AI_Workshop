import streamlit as st
from utils.pdf_utils import extract_pdf_text
from utils.parser_utils import parse_metadata_bullets, parse_authorship_response
from tools.metadata_extractor import extract_metadata
from tools.authorship_verifier import verify_authorship
from tools.impact_estimator import estimate_impact
from tools.benchmarking_agent import benchmark_paper

st.set_page_config(page_title="PDF Research Agent", layout="centered")
st.title("📄 PDF Research Agent with LangChain")

uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Extracting PDF content..."):
        text = extract_pdf_text(uploaded_file)
    st.success("PDF loaded successfully.")

    if st.button("🚀 Run All Agents"):
        with st.spinner("Running agents..."):
            metadata = extract_metadata(text)
            authorship = verify_authorship(text)
            impact = estimate_impact(text)
            benchmark = benchmark_paper(text)

        st.subheader("🧾 Metadata Extractor")
        meta_dict = parse_metadata_bullets(metadata)
        st.markdown(f"**📌 Title:** {meta_dict.get('title', 'Not found')}")
        st.markdown(f"**📄 Abstract:** {meta_dict.get('abstract', 'Not found')}")
        st.markdown("**👥 Authors:**")
        for author in meta_dict.get("authors", "").split(","):
            st.markdown(f"- {author.strip()}")

        st.markdown("**🧑 Authorship Positions:**")
        positions = {k: v for k, v in meta_dict.items() if k not in ['title', 'abstract', 'authors', 'conference/journal', 'keywords', 'year', 'doi']}
        for k, v in positions.items():
            st.markdown(f"- **{k.title()}**: {v}")
        st.markdown(f"**📚 Journal/Conference:** {meta_dict.get('conference/journal', 'Not mentioned')}")
        st.markdown(f"**📝 Keywords:** {meta_dict.get('keywords', 'Not available')}")
        st.markdown(f"**📅 Year:** {meta_dict.get('year', 'Not found')}")
        st.markdown(f"**🔗 DOI:** {meta_dict.get('doi', 'Not found')}")

        st.subheader("✍️ Authorship Verifier")
        verdict, checklist = parse_authorship_response(authorship)
        st.markdown(f"### ✅ Verdict: {verdict}")
        st.markdown("#### 📝 Evaluation Checklist")
        for item, feedback in checklist:
            st.markdown(f"- {item}: {feedback}")

        st.subheader("📈 Impact Estimator")
        st.markdown(impact)

        st.subheader("📊 Research Benchmarking (RAG)")
        st.markdown(benchmark)
    
