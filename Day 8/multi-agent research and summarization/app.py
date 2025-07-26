import streamlit as st
from graph.langgraph_workflow import build_langgraph_workflow

st.set_page_config(page_title="Multi-Agent Research Summarizer", layout="centered")
st.title("🧠 Multi-Agent Research Summarizer")

query = st.text_input("🔍 Enter your research question:")

if query:
    with st.spinner("🤖 Analyzing with AI agents..."):
        workflow = build_langgraph_workflow()
        result = workflow.invoke({"query": query})

        # Safe unpacking with fallback
        query_text = result.get("query", "")
        route = result.get("route", "N/A").replace("_", " ").title()
        summary = result.get("intermediate_result", {}).get("intermediate_result", "No summary generated.")

        # Display structured summary
        st.subheader("✅ Summary Result")
        st.markdown(f"**🔹 Query:** {query_text}")
        st.markdown(f"**🧭 Route Taken:** `{route}`")
        st.markdown("---")
        st.markdown("**📘 Final Summary:**")
        st.markdown(summary)