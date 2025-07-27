# Logistics Optimization Analysis with Crew AI

A Streamlit-based Crew AI system for analyzing logistics data and developing optimization strategies for logistics industry problems such as delivery route optimization and inventory management.

## Features
- **Crew AI Collaboration:** Two specialized agents (Logistics Analyst and Optimization Strategist) work together in a coordinated workflow.
- **Intelligent Analysis:** Comprehensive logistics operations analysis focusing on route efficiency and inventory turnover trends.
- **Strategic Optimization:** Actionable optimization strategies based on detailed analysis insights.
- **Parametrized Tasks:** Flexible product list input for customized analysis.
- **Modern UI:** Clean Streamlit interface with tabbed results and agent details.
- **Google Gemini LLM:** All analysis and strategy generation powered by Gemini (API key set directly in code).

## Folder Structure
```
logistics optimization analysis/
├── agents.py                # Crew AI agents and workflow logic
├── app.py                   # Streamlit UI with tabs
├── gemini_api.py            # Gemini API utility
├── requirements.txt         # Dependencies
├── test_crew.py             # Test suite for agents
├── screenshots/             # App screenshots
│   ├── Screenshot 2025-07-28 015815.png
│   ├── Screenshot 2025-07-28 015832.png
│   └── Screenshot 2025-07-28 015841.png
└── README.md               # This file
```

## Setup & Installation
1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **API Key:**
   - The Google Gemini API key is set directly in `gemini_api.py` (no .env file needed).
   - If you wish to use your own key, edit the `API_KEY` variable in `gemini_api.py`.

## Running the App
```sh
streamlit run app.py
```
- Open the provided local URL in your browser.
- Enter products to optimize in the sidebar.
- Select focus area (Route Optimization, Inventory Management, or Both).
- Click **Run Optimization Analysis** to execute the Crew AI workflow.

## Crew AI Workflow
1. **Logistics Analyst Agent:**
   - **Role:** Analyze current logistics operations
   - **Goal:** Identify inefficiencies in route planning and inventory management
   - **Task:** Research current state focusing on route efficiency and inventory turnover trends

2. **Optimization Strategist Agent:**
   - **Role:** Develop optimization strategies
   - **Goal:** Create actionable strategies based on analysis insights
   - **Task:** Generate optimization strategy based on Logistics Analyst findings

3. **Crew Manager:**
   - Orchestrates the collaborative workflow
   - Ensures proper data flow between agents
   - Manages the complete analysis process

## Screenshots
| Home Interface | Analysis Results | Optimization Strategy |
|----------------|------------------|----------------------|
| ![Home](screenshots/Screenshot%202025-07-28%20015815.png) | ![Analysis](screenshots/Screenshot%202025-07-28%20015832.png) | ![Strategy](screenshots/Screenshot%202025-07-28%20015841.png) |

## Sample Input & Output
**Input:**
```
Electronics (Smartphones, Laptops, Tablets)
Clothing (T-shirts, Jeans, Shoes)
Food items (Fresh produce, Dairy, Meat)
Furniture (Chairs, Tables, Beds)
```

**Output:**
- **Logistics Analysis:** Detailed analysis of current operations, bottlenecks, and inefficiencies
- **Optimization Strategy:** Comprehensive strategy including:
  - Route optimization recommendations
  - Inventory management improvements
  - Cost reduction strategies
  - Implementation timeline
  - Expected outcomes and metrics

## Testing
Run the test suite to verify all components:
```sh
python test_crew.py
```

This will test:
- Individual agent functionality
- Complete Crew AI workflow
- Gemini API integration
- Error handling

## Agent Details

### Logistics Analyst
- **Experience:** 15+ years in supply chain optimization
- **Expertise:** Route planning, warehouse operations, inventory turnover patterns
- **Focus:** Identifying bottlenecks and inefficiencies in logistics operations

### Optimization Strategist
- **Experience:** Strategic optimization expert with major corporation success
- **Expertise:** Cost reduction (20-40% improvements), efficiency enhancement
- **Focus:** Actionable strategies for operational improvement

## Technical Details
- **Frontend:** Streamlit
- **LLM:** Google Gemini API
- **Architecture:** Crew AI with collaborative agent workflow
- **API Integration:** Direct Gemini API calls (no .env) 