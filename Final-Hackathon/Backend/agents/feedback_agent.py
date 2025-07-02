import os
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from llms.llms import llm
from state.state import PitchAnalysisState
from tools import generate_final_report_tool
from typing import Dict, Any
import json

def feedback_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    """Final report generation agent using LangChain agent"""
    print("🎯 Agent 5: Final Report Generation")
    
    try:
        
        def generate_comprehensive_report(analysis_data: str) -> str:
            """Generate final report from all analysis results"""
            try:
                # Extract analysis results from state - handle proper types
                content_analysis = state.get("content_analysis", "")
                clarity_tone_analysis = state.get("clarity_tone_analysis", "")
                structure_analysis = state.get("structure_analysis", {})
                
                # Convert structure_analysis dict to string if needed
                structure_analysis_str = json.dumps(structure_analysis) if isinstance(structure_analysis, dict) else str(structure_analysis)
                
                # Validate that we have the required data
                if not content_analysis or not clarity_tone_analysis:
                    raise ValueError("Missing required analysis data")
                
                # Use the existing generate_final_report_tool
                result = generate_final_report_tool.invoke({
                    "content_analysis": content_analysis,
                    "clarity_tone_analysis": clarity_tone_analysis,
                    "structure_analysis": structure_analysis_str
                })
                
                # Return the detailed_report string from the dictionary result
                if isinstance(result, dict):
                    return result.get("detailed_report", str(result))
                return str(result)
                    
            except Exception as e:
                return f"Final report generation failed: {str(e)}"
        
        # Create the tool for LangChain agent
        report_generation_tool = Tool(
            name="GenerateFinalReport",
            func=generate_comprehensive_report,
            description="Generate comprehensive final report combining content analysis, clarity & tone analysis, and structure analysis. Provides overall scores and consolidated recommendations."
        )
        
        # Initialize the LangChain agent
        agent_executor = initialize_agent(
            tools=[report_generation_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
        
        # Prepare the input data with proper type handling
        content_analysis = state.get("content_analysis", "")
        clarity_tone_analysis = state.get("clarity_tone_analysis", "")
        structure_analysis = state.get("structure_analysis", {})
        
        # Convert structure_analysis to string for display
        structure_str = json.dumps(structure_analysis, indent=2) if isinstance(structure_analysis, dict) else str(structure_analysis)
        
        # Combine all analyses for display (trimmed to first 200 characters for preview)
        combined_input = f"Content Analysis: {content_analysis[:200] if content_analysis else 'N/A'}...\nClarity & Tone Analysis: {clarity_tone_analysis[:200] if clarity_tone_analysis else 'N/A'}...\nStructure Analysis: {structure_str[:200] if structure_str else 'N/A'}..."
        
        # Create agent instruction
        agent_instruction = f"""
        Generate a comprehensive final report by consolidating all pitch analysis results.
        
        Use the GenerateFinalReport tool to:
        - Synthesize insights from content, clarity & tone, and structure analyses
        - Provide overall pitch performance scores
        - Consolidate all recommendations into actionable feedback
        - Create a professional, well-structured final report
        - Highlight key strengths and priority improvement areas
        
        The tool will combine all previous analysis results into a cohesive final assessment.
        
        Analysis data to consolidate:
        {combined_input}
        """
        
        # Run the agent
        report_result = agent_executor.run(agent_instruction)
        
        # Generate the complete report data using the tool directly
        structure_analysis_str = json.dumps(structure_analysis) if isinstance(structure_analysis, dict) else str(structure_analysis)
        
        full_report_data = generate_final_report_tool.invoke({
            "content_analysis": content_analysis,
            "clarity_tone_analysis": clarity_tone_analysis,
            "structure_analysis": structure_analysis_str
        })
        
        # Update state with results - store as Dict[str, Any] as per state definition
        if isinstance(full_report_data, dict):
            # Add the agent's formatted text to the report data
            full_report_data["agent_report"] = report_result
            state["final_report"] = full_report_data
        else:
            # Fallback if tool doesn't return a dict
            state["final_report"] = {
                "agent_report": report_result,
                "raw_result": str(full_report_data),
                "overall_score": 0,
                "summary": "Report generation completed with fallback"
            }
        
        state["current_agent"] = "completed"
        
        # Log results
        overall_score = state["final_report"].get("overall_score", 0)
        print("✅ Final report generated")
        print(f"📊 Overall Score: {overall_score}/100")
        
        # Clean up audio file
        audio_path = state.get("audio_path")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"🧹 Deleted audio file: {audio_path}")
        
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
        print(f"❌ Error in feedback_agent: {str(e)}")
        
        # Ensure final_report is still a dict even on error
        state["final_report"] = {
            "error": str(e),
            "overall_score": 0,
            "summary": "Report generation failed"
        }
    
    return state