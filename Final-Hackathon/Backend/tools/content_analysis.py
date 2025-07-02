from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from llms.llms import llm, embedding_model
from prompts.prompt_templates import content_analysis_prompt
from typing import Dict, Any
import json

@tool
def content_analysis_tool(transcript: str, metadata: Dict[str, Any], verbose: bool = False) -> str:
    """Analyze content structure and relevance using RAG with pre-loaded pitch templates"""
    
    try:
        # Load FAISS vector store
        retriever = FAISS.load_local(
            "faiss_index",
            embedding_model,
            allow_dangerous_deserialization=True
        ).as_retriever()
        
        # Create RAG chain
        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": content_analysis_prompt}
        )
        
        # Prepare metadata string
        metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
        
        # Create pitch content for analysis - RAG will retrieve relevant templates
        pitch_content = f"Transcript:\n{transcript}\n\nVideo Metadata:\n{metadata_str}"
        
        if verbose:
            print(f"📝 Analyzing pitch content with {len(transcript)} characters of transcript")
            print(f"📊 Using RAG system with pre-loaded pitch templates")
        
        # Run the analysis
        result = rag_chain.invoke({"query": pitch_content})
        analysis_result = result.get("result", str(result))
        
        if verbose:
            print("✅ Content analysis completed successfully")
        
        return analysis_result
        
    except Exception as e:
        error_msg = f"Content analysis failed: {str(e)}"
        if verbose:
            print(f"❌ {error_msg}")
        return error_msg