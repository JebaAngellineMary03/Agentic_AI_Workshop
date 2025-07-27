from gemini_api import gemini_generate

class LogisticsAnalyst:
    def __init__(self):
        self.role = "Logistics Analyst"
        self.goal = "Analyze current logistics operations and identify inefficiencies in route planning and inventory management"
        self.backstory = """You are an experienced logistics analyst with 15+ years in supply chain optimization. 
        You specialize in analyzing delivery routes, warehouse operations, and inventory turnover patterns. 
        Your expertise lies in identifying bottlenecks and inefficiencies in logistics operations."""
    
    def analyze_logistics_operations(self, products_list):
        """Analyze current logistics operations focusing on route efficiency and inventory turnover"""
        prompt = f"""
        As a Logistics Analyst, analyze the current state of logistics operations for the following products: {products_list}
        
        Focus on:
        1. Route efficiency analysis
        2. Inventory turnover trends
        3. Current bottlenecks and inefficiencies
        4. Cost analysis of current operations
        
        Provide a detailed analysis with specific insights and data points.
        """
        return gemini_generate(prompt)

class OptimizationStrategist:
    def __init__(self):
        self.role = "Optimization Strategist"
        self.goal = "Develop comprehensive optimization strategies based on logistics analysis to improve efficiency and reduce costs"
        self.backstory = """You are a strategic optimization expert with deep knowledge of logistics systems. 
        You have successfully implemented optimization strategies for major corporations, reducing costs by 20-40% 
        while improving delivery times and customer satisfaction."""
    
    def create_optimization_strategy(self, logistics_analysis, products_list):
        """Create optimization strategy based on logistics analysis insights"""
        prompt = f"""
        As an Optimization Strategist, create a comprehensive optimization strategy based on this logistics analysis:
        
        LOGISTICS ANALYSIS:
        {logistics_analysis}
        
        PRODUCTS TO OPTIMIZE:
        {products_list}
        
        Develop a strategy that includes:
        1. Route optimization recommendations
        2. Inventory management improvements
        3. Cost reduction strategies
        4. Implementation timeline
        5. Expected outcomes and metrics
        
        Provide actionable recommendations with specific steps.
        """
        return gemini_generate(prompt)

class CrewManager:
    def __init__(self):
        self.logistics_analyst = LogisticsAnalyst()
        self.optimization_strategist = OptimizationStrategist()
    
    def run_optimization_analysis(self, products_list):
        """Execute the complete crew workflow"""
        # Step 1: Logistics Analysis
        logistics_analysis = self.logistics_analyst.analyze_logistics_operations(products_list)
        
        # Step 2: Optimization Strategy
        optimization_strategy = self.optimization_strategist.create_optimization_strategy(
            logistics_analysis, products_list
        )
        
        return {
            "logistics_analysis": logistics_analysis,
            "optimization_strategy": optimization_strategy
        } 