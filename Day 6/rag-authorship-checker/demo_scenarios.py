DEMO_SCENARIOS = {
    "legitimate_paper": {
        "title": "Machine Learning Approaches to Climate Data Analysis",
        "authors": ["Emily Rodriguez", "Dr. James Park", "Prof. Lisa Chen"],
        "claimed_author": "Emily Rodriguez",
        "description": "High-quality student research with proper authorship",
        "expected_outcome": "Should pass verification with high quality score"
    },
    
    "ai_generated": {
        "title": "Comprehensive Analysis of Artificial Intelligence Applications",
        "authors": ["Alex Thompson"],
        "claimed_author": "Alex Thompson",
        "content": """In conclusion, it is important to note that this comprehensive 
        analysis delves into the intricate and multifaceted aspects of artificial 
        intelligence. Furthermore, the nuanced understanding of these complex 
        algorithms requires delving into the multifaceted nature of machine learning. 
        Moreover, it should be noted that the comprehensive evaluation of AI systems 
        provides intricate insights into the delicate balance of technological advancement.""",
        "description": "Paper with high AI-generated content probability",
        "expected_outcome": "Should flag high AI probability"
    },
    
    "authorship_issue": {
        "title": "Advanced Neural Network Architectures for Computer Vision",
        "authors": ["Dr. Michael Johnson", "Prof. Sarah Davis", "Research Team"],
        "claimed_author": "Student X",
        "description": "Student claiming authorship of faculty paper",
        "expected_outcome": "Should fail authorship verification"
    },
    
    "doi_example": {
        "doi": "10.1038/nature12373",
        "claimed_author": "John Student",
        "description": "Real paper DOI - should detect authorship mismatch",
        "expected_outcome": "Should fail authorship verification"
    }
}

def get_demo_scenario(scenario_name):
    """Get a demo scenario by name"""
    return DEMO_SCENARIOS.get(scenario_name, {})

def list_scenarios():
    """List available demo scenarios"""
    print("Available Demo Scenarios:")
    print("="*30)
    for name, scenario in DEMO_SCENARIOS.items():
        print(f"📋 {name}")
        print(f"   Description: {scenario['description']}")
        print(f"   Expected: {scenario['expected_outcome']}")
        print()

if __name__ == "__main__":
    list_scenarios()
