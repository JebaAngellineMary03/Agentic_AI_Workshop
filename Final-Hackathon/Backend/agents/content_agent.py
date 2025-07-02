from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from llms.llms import llm, embedding_model
from prompts.prompt_templates import content_analysis_prompt
from state.state import PitchAnalysisState
from typing import Dict, Any
import json

def content_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    """Content analysis agent using LangChain agent with pitch templates"""
    print("📊 Agent 2: Content Analysis")
    
    try:
        
        def analyze_pitch_against_templates(transcript_and_metadata: str) -> str:
            """Analyze pitch content against the pitch templates using RAG"""
            try:
                # Load FAISS vector store
                retriever = FAISS.load_local(
                    "faiss_index",
                    embedding_model,
                    allow_dangerous_deserialization=True
                ).as_retriever()
                
                # Create RAG chain with your existing prompt
                rag_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=retriever,
                    chain_type="stuff",
                    chain_type_kwargs={"prompt": content_analysis_prompt}
                )
                
                # The RAG system will automatically retrieve relevant pitch templates
                # No need to manually add template context
                enhanced_query = transcript_and_metadata
                
                # Run the analysis
                result = rag_chain.invoke({"query": enhanced_query})
                return result.get("result", str(result))
                
            except Exception as e:
                return f"RAG-based content analysis failed: {str(e)}"
        
        # Create the tool for LangChain agent
        content_analysis_tool = Tool(
            name="AnalyzePitchContent",
            func=analyze_pitch_against_templates,
            description="Analyze pitch transcript and metadata using RAG system with loaded pitch templates. Input should be the combined transcript and metadata."
        )
        
        # Initialize the LangChain agent
        agent_executor = initialize_agent(
            tools=[content_analysis_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
        
        # Prepare the input data
        transcript = state.get("transcript", "")
        metadata = state.get("metadata", {})
        metadata_str = "\n".join(f"{k}: {v}" for k, v in metadata.items())
        
        # Combine transcript and metadata
        combined_input = f"Transcript:\n{transcript}\n\nVideo Metadata:\n{metadata_str}"
        
        # Create agent instruction
        agent_instruction = f"""
        Analyze this pitch content using the RAG system which has pitch templates already loaded.
        
        Use the AnalyzePitchContent tool to evaluate:
        - How well the pitch follows effective structure from loaded templates
        - Content relevance and focus based on best practices
        - Missing sections or opportunities
        - Specific improvement suggestions
        
        The RAG system will automatically retrieve relevant pitch templates for comparison.
        
        Pitch content to analyze:
        {combined_input[:1000]}{'...' if len(combined_input) > 1000 else ''}
        """
        
        # Run the agent
        analysis_result = agent_executor.run(agent_instruction)
        
        # Update state with results
        state["content_analysis"] = analysis_result
        state["current_agent"] = "clarity_agent"
        print("✅ Content analysis completed")
        
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error_handler"
        print(f"❌ Error in content_agent: {str(e)}")
    
    return state
