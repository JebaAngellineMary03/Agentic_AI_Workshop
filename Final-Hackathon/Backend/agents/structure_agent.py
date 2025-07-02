from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from llms.llms import llm
from state.state import PitchAnalysisState
from tools import structure_analysis_tool
from typing import Dict, Any

def structure_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    """Structure analysis agent using LangChain agent"""
    print("🏗️ Agent 4: Structure Analysis")
    
    try:
        
        def analyze_pitch_structure(transcript_metadata: str) -> str:
            """Analyze pitch structure from transcript and metadata"""
            try:
                # Extract transcript and metadata from state directly
                transcript = state.get("transcript", "")
                metadata = state.get("metadata", {})
                
                # Use the existing structure_analysis_tool
                result = structure_analysis_tool.invoke({
                    "transcript": transcript,
                    "metadata": metadata,
                    "verbose": True
                })
                
                return result
                    
            except Exception as e:
                return f"Structure analysis failed: {str(e)}"
        
        # Create the tool for LangChain agent
        structure_tool = Tool(
            name="AnalyzePitchStructure",
            func=analyze_pitch_structure,
            description="Analyze pitch structure from transcript and metadata. Evaluates pitch organization, flow, key sections, and structural improvements."
        )
        
        # Initialize the LangChain agent
        agent_executor = initialize_agent(
            tools=[structure_tool],
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
        
        # Combine transcript and metadata for display
        combined_input = f"Transcript: {transcript}\nMetadata: {metadata_str}"
        
        # Create agent instruction
        agent_instruction = f"""
        Analyze the structure and organization of this pitch presentation.
        
        Use the AnalyzePitchStructure tool to evaluate:
        - Overall pitch structure and flow
        - Presence of key pitch sections (problem, solution, market, etc.)
        - Logical sequence and transitions between sections
        - Missing structural elements
        - Recommendations for better organization
        
        The tool will analyze both the transcript content and video metadata to provide comprehensive structural analysis.
        
        Pitch content to analyze:
        {combined_input[:500]}{'...' if len(combined_input) > 500 else ''}
        """
        
        # Run the agent
        analysis_result = agent_executor.run(agent_instruction)
        
        # Update state with results
        state["structure_analysis"] = analysis_result
        state["current_agent"] = "feedback_agent"
        print("✅ Structure analysis completed")
        
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
        print(f"❌ Error in structure_agent: {str(e)}")
    
    return state