from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from llms.llms import llm
from state.state import PitchAnalysisState
from tools import clarity_tone_analysis_tool
from typing import Dict, Any

def clarity_agent(state: PitchAnalysisState) -> PitchAnalysisState:
    """Clarity and tone analysis agent using LangChain agent"""
    print("🎤 Agent 3: Clarity & Tone Analysis")
    
    try:
        
        def analyze_speech_clarity_tone(combined_data: str) -> str:
            """Analyze speech clarity and tone using audio processing and transcript analysis"""
            try:
                # Extract transcript, audio_path, and audio_features from state directly
                # The combined_data contains the formatted input for reference
                transcript = state.get("transcript", "")
                audio_path = state.get("audio_path", "")
                audio_features = state.get("audio_features", {})
                
                # Use the existing clarity_tone_analysis_tool
                result = clarity_tone_analysis_tool.invoke({
                    "transcript": transcript,
                    "audio_path": audio_path,
                    "audio_features": audio_features
                })
                
                return result
                    
            except Exception as e:
                return f"Clarity and tone analysis failed: {str(e)}"
        
        # Create the tool for LangChain agent
        clarity_tone_tool = Tool(
            name="AnalyzeSpeechClarityTone",
            func=analyze_speech_clarity_tone,
            description="Analyze speech clarity and tone from transcript, audio path, and audio features. Provides clarity score (0-100), tone score (0-100), and improvement recommendations."
        )
        
        # Initialize the LangChain agent
        agent_executor = initialize_agent(
            tools=[clarity_tone_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
        
        # Prepare the input data
        transcript = state.get("transcript", "")
        audio_path = state.get("audio_path", "")
        audio_features = state.get("audio_features", {})
        
        # Convert audio features to string for tool input
        import json
        audio_features_str = json.dumps(audio_features) if audio_features else "{}"
        
        # Combine all data for the agent instruction (simplified)
        combined_input = f"Transcript: {transcript}\nAudio Path: {audio_path}\nAudio Features: {audio_features_str}"
        
        # Create agent instruction
        agent_instruction = f"""
        Analyze the speech clarity and tone for this pitch recording.
        
        Use the AnalyzeSpeechClarityTone tool to evaluate:
        - Speech clarity score (0-100) based on audio processing
        - Tone quality score (0-100) based on vocal characteristics
        - Specific feedback on speech delivery
        - Actionable recommendations for improvement
        - Audio feature analysis (tempo, pitch, loudness, etc.)
        
        The tool will process both the transcript text and audio features to provide comprehensive analysis.
        
        Speech data to analyze:
        {combined_input[:500]}{'...' if len(combined_input) > 500 else ''}
        """
        
        # Run the agent
        analysis_result = agent_executor.run(agent_instruction)
        
        # Update state with results
        state["clarity_tone_analysis"] = analysis_result
        state["current_agent"] = "structure_agent"
        print("✅ Clarity & tone analysis completed")
        
    except Exception as e:
        state["error_message"] = str(e)
        state["current_agent"] = "error"
        print(f"❌ Error in clarity_agent: {str(e)}")
    
    return state