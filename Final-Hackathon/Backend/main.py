import logging
import traceback
from state.state import PitchAnalysisState
from graph.graph import create_pitch_analysis_graph
from typing import Annotated

# Set up logging to see all output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pitch_analysis(youtube_url: str) -> PitchAnalysisState:
    """Runs the full pitch analysis LangGraph pipeline"""
    
    logger.info(f"🚀 Starting pitch analysis for URL: {youtube_url}")
    print(f"🚀 Starting pitch analysis for URL: {youtube_url}")
    
    try:
        app = create_pitch_analysis_graph()
        logger.info("✅ Graph created successfully")
        print("✅ Graph created successfully")
        
        # Initialize the state
        initial_state = PitchAnalysisState(
            youtube_url=youtube_url,
            transcript="",
            metadata={},
            audio_features={},
            audio_path="",
            content_analysis="",
            clarity_tone_analysis="",
            structure_analysis={},
            final_report={},
            current_agent="start",
            error_message="",
            retry_count=0
        )
        
        logger.info("✅ Initial state created")
        print("✅ Initial state created")
        
        # Initialize final_state with initial_state to ensure it's always defined
        final_state = initial_state
        logger.info("✅ Final state initialized")
        print("✅ Final state initialized")
        
        try:
            logger.info("🔄 Starting workflow execution...")
            print("🔄 Starting workflow execution...")
            
            # Run the workflow
            final_state = app.invoke(initial_state)
            
            logger.info("✅ Workflow execution completed")
            print("✅ Workflow execution completed")
            
            # Check if analysis was successful
            current_agent = final_state.get("current_agent", "unknown")
            logger.info(f"📊 Current agent status: {current_agent}")
            print(f"📊 Current agent status: {current_agent}")
            
            if current_agent == "completed":
                logger.info("🎉 Analysis completed successfully")
                print("🎉 Analysis completed successfully")
                
                print("\n" + "="*60)
                print("🎉 PITCH ANALYSIS COMPLETED")
                print("="*60)
                
                report = final_state.get("final_report", {})
                print(f"\n🎯 OVERALL SCORE: {report.get('overall_score', 'N/A')}/100")
                print("="*60)
                
                scores = report.get('scores', {})
                print(f"\n📊 INDIVIDUAL SCORES:")
                print(f"   • Content: {scores.get('content', 'N/A')}/100")
                print(f"   • Clarity: {scores.get('clarity', 'N/A')}/100")
                print(f"   • Tone: {scores.get('tone', 'N/A')}/100")
                print(f"   • Structure: {scores.get('structure_flow', 'N/A')}/100")
                
                print(f"\n📝 DETAILED REPORT:")
                print(report.get('detailed_report', 'No detailed report available'))
            else:
                error_message = final_state.get('error_message', 'Unknown error')
                logger.error(f"❌ Analysis failed: {error_message}")
                print(f"\n❌ Analysis failed: {error_message}")
                
        except Exception as workflow_error:
            logger.error(f"💥 Workflow execution failed: {str(workflow_error)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            print(f"\n💥 Workflow execution failed: {str(workflow_error)}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # Handle workflow exception
            if isinstance(final_state, dict):
                final_state = final_state.copy()
            else:
                # Convert to dict if it's a state object
                final_state = dict(final_state) if hasattr(final_state, '__dict__') else {}
            
            final_state["current_agent"] = "failed"
            final_state["error_message"] = str(workflow_error)
            
    except Exception as setup_error:
        logger.error(f"💥 Setup failed: {str(setup_error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print(f"💥 Setup failed: {str(setup_error)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Return error state
        final_state = {
            "youtube_url": youtube_url,
            "transcript": "",
            "metadata": {},
            "audio_features": {},
            "audio_path": "",
            "content_analysis": "",
            "clarity_tone_analysis": "",
            "structure_analysis": {},
            "final_report": {},
            "current_agent": "failed",
            "error_message": str(setup_error),
            "retry_count": 0
        }
    
    logger.info(f"🏁 Returning final state with agent: {final_state.get('current_agent', 'unknown')}")
    print(f"🏁 Returning final state with agent: {final_state.get('current_agent', 'unknown')}")
    
    return final_state

if __name__ == "__main__":
    import uvicorn
    from app import app
    uvicorn.run(app, host="0.0.0.0", port=8000)