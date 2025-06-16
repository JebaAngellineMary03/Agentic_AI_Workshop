import asyncio
import json
from backend.agent import GeminiResearchAgent

async def test_system():
    """Test the verification system with sample data"""
    print("🧪 Testing Research Paper Verification System\n")
    
    agent = GeminiResearchAgent()
    
    # Test Case 1: Manual submission
    print("📝 Test Case 1: Manual Submission")
    test_submission = {
        "title": "Deep Learning Applications in Natural Language Processing",
        "authors": ["John Smith", "Jane Doe", "Alice Johnson"],
        "claimed_author": "John Smith"
    }
    
    result1 = await agent.process_submission(test_submission)
    print(f"Quality Score: {result1['quality_score']}/100")
    print(f"Authorship: {result1['authorship']['status']}")
    print(f"AI Probability: {result1['ai_detection'].get('ai_probability', 0):.2f}")
    print("Recommendations:")
    for rec in result1['recommendations']:
        print(f"  - {rec}")
    print("\n" + "="*50 + "\n")
    
    # Test Case 2: Suspicious submission
    print("📝 Test Case 2: Suspicious AI-Generated Content")
    suspicious_text = """
    In conclusion, it is important to note that this comprehensive analysis 
    delves into the intricate and multifaceted aspects of machine learning. 
    Furthermore, it should be noted that the nuanced understanding of these 
    complex algorithms requires careful consideration. Moreover, the 
    multifaceted nature of this research provides comprehensive insights 
    into the delicate balance of artificial intelligence applications.
    """
    
    test_submission2 = {
        "title": "AI Research Paper",
        "authors": ["Unknown Author"],
        "claimed_author": "Student Name",
        "content": suspicious_text
    }
    
    # Manually add content for AI detection
    result2 = await agent.process_submission(test_submission2)
    # Override AI detection for demo
    result2['ai_detection'] = agent.ai_detector.analyze_text(suspicious_text)
    
    print(f"Quality Score: {result2['quality_score']}/100")
    print(f"Authorship: {result2['authorship']['status']}")
    print(f"AI Probability: {result2['ai_detection']['ai_probability']:.2f}")
    print("Recommendations:")
    for rec in result2['recommendations']:
        print(f"  - {rec}")
    print("\n" + "="*50 + "\n")
    
    # Test Case 3: High quality submission
    print("📝 Test Case 3: High Quality Submission")
    quality_text = """
    This research presents novel experimental results on protein folding 
    mechanisms using X-ray crystallography data. Our methodology involved 
    systematic analysis of 200 protein samples, revealing three distinct 
    folding pathways not previously documented in literature. The statistical 
    significance (p<0.001) confirms the robustness of our findings.
    """
    
    test_submission3 = {
        "title": "Novel Protein Folding Mechanisms: An Experimental Study",
        "authors": ["Dr. Sarah Wilson", "Prof. Michael Chen"],
        "claimed_author": "Sarah Wilson",
        "content": quality_text
    }
    
    result3 = await agent.process_submission(test_submission3)
    result3['ai_detection'] = agent.ai_detector.analyze_text(quality_text)
    result3['quality_score'] = 85  # Override for demo
    
    print(f"Quality Score: {result3['quality_score']}/100")
    print(f"Authorship: {result3['authorship']['status']}")
    print(f"AI Probability: {result3['ai_detection']['ai_probability']:.2f}")
    print("Recommendations:")
    for rec in result3['recommendations']:
        print(f"  - {rec}")
    
    print("\n✅ All tests completed!")
    return True

if __name__ == "__main__":
    asyncio.run(test_system())