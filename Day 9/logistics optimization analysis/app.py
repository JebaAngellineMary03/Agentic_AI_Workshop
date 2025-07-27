import streamlit as st
from agents import CrewManager

st.set_page_config(page_title="Logistics Optimization Analysis", layout="wide")
st.title("🚚 Logistics Optimization Analysis with Crew AI")

if 'crew_results' not in st.session_state:
    st.session_state['crew_results'] = None

# Sidebar for input
with st.sidebar:
    st.header("📋 Input Parameters")
    
    # Product list input
    products_input = st.text_area(
        "Enter products to optimize (one per line or comma-separated):",
        placeholder="e.g., Electronics, Clothing, Food items, Furniture",
        height=150
    )
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Focus Area:",
        ["Route Optimization", "Inventory Management", "Both"]
    )
    
    if st.button("🚀 Run Optimization Analysis"):
        if products_input.strip():
            # Process products list
            products_list = [p.strip() for p in products_input.replace('\n', ',').split(',') if p.strip()]
            
            with st.spinner("Running Crew AI analysis..."):
                crew_manager = CrewManager()
                results = crew_manager.run_optimization_analysis(products_list)
                st.session_state['crew_results'] = results
            st.success("Analysis completed!")
        else:
            st.error("Please enter at least one product to analyze.")

# Main content area
if st.session_state['crew_results']:
    results = st.session_state['crew_results']
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Logistics Analysis", "🎯 Optimization Strategy", "👥 Agent Details"])
    
    with tab1:
        st.header("Logistics Analysis Results")
        st.markdown(results['logistics_analysis'])
    
    with tab2:
        st.header("Optimization Strategy")
        st.markdown(results['optimization_strategy'])
    
    with tab3:
        st.header("Crew AI Agent Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 Logistics Analyst")
            st.markdown("""
            **Role:** Logistics Analyst  
            **Goal:** Analyze current logistics operations and identify inefficiencies  
            **Expertise:** Route planning, warehouse operations, inventory turnover patterns
            """)
        
        with col2:
            st.subheader("🎯 Optimization Strategist")
            st.markdown("""
            **Role:** Optimization Strategist  
            **Goal:** Develop comprehensive optimization strategies  
            **Expertise:** Cost reduction, efficiency improvement, strategic planning
            """)
        
        st.subheader("🔄 Workflow Process")
        st.markdown("""
        1. **Logistics Analyst** analyzes current operations and identifies inefficiencies
        2. **Optimization Strategist** creates actionable strategies based on analysis
        3. **Crew Manager** orchestrates the collaborative workflow
        """)

# Sample data for demonstration
if not st.session_state['crew_results']:
    st.info("👈 Use the sidebar to input products and run the optimization analysis.")
    
    st.subheader("📝 Sample Input")
    st.code("""
Electronics (Smartphones, Laptops, Tablets)
Clothing (T-shirts, Jeans, Shoes)
Food items (Fresh produce, Dairy, Meat)
Furniture (Chairs, Tables, Beds)
    """)
    
    st.subheader("🎯 What This System Does")
    st.markdown("""
    - **Analyzes** current logistics operations for efficiency
    - **Identifies** bottlenecks and cost optimization opportunities
    - **Develops** actionable strategies for improvement
    - **Provides** route optimization and inventory management recommendations
    """) 