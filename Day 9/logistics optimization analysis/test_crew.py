from agents import LogisticsAnalyst, OptimizationStrategist, CrewManager

def test_logistics_analyst():
    """Test the Logistics Analyst agent"""
    print("🧪 Testing Logistics Analyst...")
    analyst = LogisticsAnalyst()
    
    # Test with sample products
    sample_products = ["Electronics", "Clothing", "Food items"]
    analysis = analyst.analyze_logistics_operations(sample_products)
    
    print(f"✅ Logistics Analysis completed!")
    print(f"📊 Analysis length: {len(analysis)} characters")
    print(f"📝 First 200 chars: {analysis[:200]}...")
    return analysis

def test_optimization_strategist():
    """Test the Optimization Strategist agent"""
    print("\n🧪 Testing Optimization Strategist...")
    strategist = OptimizationStrategist()
    
    # Mock logistics analysis
    mock_analysis = "Sample logistics analysis showing inefficiencies in route planning and inventory management."
    sample_products = ["Electronics", "Clothing", "Food items"]
    
    strategy = strategist.create_optimization_strategy(mock_analysis, sample_products)
    
    print(f"✅ Optimization Strategy completed!")
    print(f"📊 Strategy length: {len(strategy)} characters")
    print(f"📝 First 200 chars: {strategy[:200]}...")
    return strategy

def test_crew_workflow():
    """Test the complete crew workflow"""
    print("\n🧪 Testing Complete Crew Workflow...")
    crew_manager = CrewManager()
    
    # Test with sample products
    sample_products = ["Electronics", "Clothing", "Food items", "Furniture"]
    results = crew_manager.run_optimization_analysis(sample_products)
    
    print(f"✅ Complete workflow completed!")
    print(f"📊 Results keys: {list(results.keys())}")
    print(f"📝 Logistics Analysis length: {len(results['logistics_analysis'])} characters")
    print(f"📝 Optimization Strategy length: {len(results['optimization_strategy'])} characters")
    
    return results

def main():
    """Run all tests"""
    print("🚚 Logistics Optimization Analysis - Crew AI Test Suite")
    print("=" * 60)
    
    try:
        # Test individual agents
        logistics_analysis = test_logistics_analyst()
        optimization_strategy = test_optimization_strategist()
        
        # Test complete workflow
        crew_results = test_crew_workflow()
        
        print("\n🎉 All tests passed successfully!")
        print("\n📋 Summary:")
        print(f"- Logistics Analyst: ✅ Working")
        print(f"- Optimization Strategist: ✅ Working")
        print(f"- Crew Workflow: ✅ Working")
        print(f"- Gemini API Integration: ✅ Working")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Ready to run the Streamlit app!")
    else:
        print("\n❌ Please check your setup and try again.") 