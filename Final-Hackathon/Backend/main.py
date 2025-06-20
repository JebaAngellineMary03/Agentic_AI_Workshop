from state.state import PitchAnalysisState
from graph.graph import create_pitch_analysis_graph  # Assum
import uvicorn
from app import app


def run_pitch_analysis(youtube_url: str):
    """Run the complete pitch analysis workflow"""
    
    # Create the graph
    app = create_pitch_analysis_graph()
    
    # Initial state
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
    
    # Run the workflow
    try:
        final_state = app.invoke(initial_state)
        
        if final_state["current_agent"] == "completed":
            print("\n" + "="*60)
            print("🎉 PITCH ANALYSIS COMPLETED")
            print("="*60)
            
            report = final_state["final_report"]
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
            
            return final_state
            
        else:
            print(f"\n❌ Analysis failed: {final_state.get('error_message', 'Unknown error')}")
            return final_state
            
    except Exception as e:
        print(f"\n💥 Workflow execution failed: {str(e)}")
        return None


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
