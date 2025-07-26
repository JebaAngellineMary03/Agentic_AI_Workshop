# 🧠 Competitor Search Agent with Gemini 1.5 Flash + LangChain

This project uses **LangChain Agents** powered by **Google Gemini 1.5 Flash** to search for clothing competitors and analyze footfall trends in a given location.

> ⚡ **Gemini 1.5 Flash** provides blazing-fast, cost-effective reasoning—ideal for real-time AI agents.

---

## 🚀 Features

- ✅ **Gemini 1.5 Flash LLM** via Google Generative AI API  
- ✅ **LangChain Agent** with `ZERO_SHOT_REACT_DESCRIPTION`  
- ✅ **Custom Tool**: `SearchCompetitors`  
- ✅ `.env` support for secure API key management  
- ✅ Error handling and limited iteration control via `max_iterations=5`

---

## 📁 Folder Structure
├── main.py # LangChain agent logic
├── tools.py # Custom tools like search_competitors
├── .env # API key (excluded from Git)
├── requirements.txt # Python dependencies
└── README.md # This file

## 🛠️ Installation & Setup

<pre># 1. Clone the repository
git clone https://github.com/yourname/competitor-agent.git
cd competitor-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key to a .env file
echo "GEMINI_API_KEY=your-google-api-key" > .env

# 4. Run the agent
python main.py</pre>

# 🧪 Example Prompt
### Prompt:
<pre> Can you find the top clothing competitors and footfall trends in Coimbatore? 

Agent Response:
> Entering new AgentExecutor chain...
Thought: I need to use the SearchCompetitors tool.
Action: SearchCompetitors
Action Input: "Coimbatore"
Observation: Top 3 competitors in Coimbatore: Reliance Trends, Pantaloons, Max Fashion. Footfall highest during weekends.
Final Answer: The top clothing competitors in Coimbatore are Reliance Trends, Pantaloons, and Max Fashion. </pre>

