from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from llms.llms import llm, embedding_model
from prompts.prompt_templates import content_analysis_prompt
from typing import Dict, Any

@tool
def content_analysis_tool(transcript: str, metadata: Dict[str, Any]) -> str:
    """Analyze content structure and relevance using RAG"""
    try:
        retriever = FAISS.load_local(
            "faiss_index",
            embedding_model,
            allow_dangerous_deserialization=True
        ).as_retriever()

        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": content_analysis_prompt}
        )

        metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
        pitch_content = f"Transcript:\n{transcript}\n\nVideo Metadata:\n{metadata_str}"

        result = rag_chain.invoke({"query": pitch_content})
        return result.get("result", str(result))

    except Exception as e:
        return f"Content analysis failed: {str(e)}"
