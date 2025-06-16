import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Research Paper Verification System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Research Paper Verification System")
st.markdown("### Automated verification of student research submissions")

# Sidebar for input method selection
st.sidebar.header("Input Method")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["DOI/URL", "PDF Upload", "Manual Entry"]
)

# Main interface
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Paper Submission")
    
    if input_method == "DOI/URL":
        doi = st.text_input("Enter DOI or URL:")
        claimed_author = st.text_input("Claimed Author Name:")
        
        if st.button("Verify Paper") and doi:
            with st.spinner("Analyzing paper..."):
                # Call backend API
                response = requests.post(
                    "http://localhost:8000/verify-paper",
                    json={
                        "doi": doi,
                        "claimed_author": claimed_author
                    }
                )
                
                if response.status_code == 200:
                    st.session_state.results = response.json()
                else:
                    st.error("Failed to analyze paper")
    
    elif input_method == "PDF Upload":
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        claimed_author = st.text_input("Claimed Author Name:")
        
        if st.button("Analyze PDF") and uploaded_file:
            with st.spinner("Processing PDF..."):
                files = {"file": uploaded_file.getvalue()}
                data = {"claimed_author": claimed_author}
                
                response = requests.post(
                    "http://localhost:8000/upload-pdf",
                    files={"file": uploaded_file},
                    data={"claimed_author": claimed_author}
                )
                
                if response.status_code == 200:
                    st.session_state.results = response.json()
                else:
                    st.error("Failed to process PDF")
    
    elif input_method == "Manual Entry":
        title = st.text_input("Paper Title:")
        authors = st.text_area("Authors (one per line):").split('\n')
        claimed_author = st.text_input("Claimed Author Name:")
        
        if st.button("Verify Submission") and title:
            with st.spinner("Verifying submission..."):
                response = requests.post(
                    "http://localhost:8000/verify-paper",
                    json={
                        "title": title,
                        "authors": [a.strip() for a in authors if a.strip()],
                        "claimed_author": claimed_author
                    }
                )
                
                if response.status_code == 200:
                    st.session_state.results = response.json()
                else:
                    st.error("Failed to verify submission")

# Results display
with col2:
    st.header("📊 Analysis Results")
    
    if 'results' in st.session_state:
        results = st.session_state.results
        
        # Quality Score
        quality_score = results.get('quality_score', 0)
        st.metric("Overall Quality Score", f"{quality_score}/100")
        
        # Progress bars for different metrics
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Authorship verification
            auth_status = results.get('authorship', {}).get('status', 'unknown')
            auth_confidence = results.get('authorship', {}).get('confidence', 0)
            
            st.subheader("👤 Authorship Verification")
            if auth_status == 'verified':
                st.success(f"✅ Verified ({auth_confidence:.0%} confidence)")
            else:
                st.warning(f"⚠️ Not verified ({auth_confidence:.0%} confidence)")
        
        with col_b:
            # AI Detection
            ai_prob = results.get('ai_detection', {}).get('ai_probability', 0)
            st.subheader("🤖 AI Detection")
            
            if ai_prob > 0.7:
                st.error(f"🚨 High AI probability ({ai_prob:.0%})")
            elif ai_prob > 0.4:
                st.warning(f"⚠️ Moderate AI probability ({ai_prob:.0%})")
            else:
                st.success(f"✅ Low AI probability ({ai_prob:.0%})")
            
            st.progress(ai_prob)
        
        # Detailed Analysis
        st.subheader("📋 Detailed Analysis")
        
        # Paper Information
        with st.expander("📄 Paper Information", expanded=True):
            paper_info = results.get('paper_info', {})
            st.write(f"**Title:** {paper_info.get('title', 'N/A')}")
            authors = paper_info.get('authors', [])
            if authors:
                st.write(f"**Authors:** {', '.join(authors)}")
            else:
                st.write("**Authors:** Not available")
        
        # Similar Papers
        similar_papers = results.get('similar_papers', [])
        if similar_papers:
            with st.expander("🔍 Similar Papers Found"):
                for i, paper in enumerate(similar_papers[:3]):  # Show top 3
                    st.write(f"**{i+1}.** {paper.get('title', 'Unknown')}")
                    st.write(f"*Authors:* {', '.join(paper.get('authors', []))}")
                    st.write(f"*Similarity:* {paper.get('similarity', 0):.2f}")
                    st.write("---")
        
        # Recommendations
        recommendations = results.get('recommendations', [])
        if recommendations:
            st.subheader("💡 Mentor Recommendations")
            for rec in recommendations:
                if "✅" in rec:
                    st.success(rec)
                elif "❌" in rec or "🚨" in rec:
                    st.error(rec)
                else:
                    st.warning(rec)
        
        # Flags
        flags = results.get('flags', [])
        if flags:
            st.subheader("🚩 Flags & Alerts")
            for flag in flags:
                st.error(f"⚠️ {flag}")
        
        # Raw Results (for debugging)
        with st.expander("🔧 Technical Details"):
            st.json(results)
    
    else:
        st.info("👆 Please submit a paper for analysis using the form on the left.")
        
        # Show demo instructions
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        1. **Choose input method** from the sidebar
        2. **DOI/URL**: Enter paper DOI or URL
        3. **PDF Upload**: Upload paper PDF file
        4. **Manual Entry**: Enter paper details manually
        5. **Enter claimed author** name for verification
        6. **Click analyze** to get comprehensive results
        
        ### 📊 What You'll Get
        - **Quality Score**: Overall paper assessment
        - **Authorship Verification**: Check claimed authorship
        - **AI Detection**: Identify potentially AI-generated content
        - **Similar Papers**: Find related research
        - **Mentor Recommendations**: Actionable guidance
        """)

# Footer
st.markdown("---")
st.markdown("Built for academic integrity verification | Hackathon Demo")