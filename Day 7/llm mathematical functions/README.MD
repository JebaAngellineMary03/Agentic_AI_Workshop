# 🧠 LangGraph General + Math Agent

A **LangGraph-powered multi-tool agent** built with **Streamlit UI** that handles both **natural language queries** and **mathematical calculations**. It intelligently routes inputs between a Gemini-powered LLM and custom math tool functions.

---

## 📁 Project Structure

langgraph-agent/
│
├── agents/
│ └── math_general_agent.py # LangGraph agent and workflow definition
│
├── services/
│ └── gemini_api.py # Gemini API integration for LLM responses
│
├── tools/
│ └── math_tools.py # Custom math tools: add, subtract, multiply, divide
│
├── .env # Environment file with your GEMINI/GOOGLE API key
├── main.py # Streamlit UI for interacting with the agent
├── requirements.txt # Python dependencies
└── README.md # You're reading it!

yaml
Copy
Edit

---

## 🚀 Features

- 🔄 **LangGraph Workflow**: Routes inputs between LLM and math tools based on input analysis.  
- 🤖 **Gemini LLM**: Handles open-ended or general knowledge queries using Google's Gemini API.  
- ➕ **Custom Math Tools**: Performs basic arithmetic operations like `add`, `subtract`, `multiply`, and `divide`.  
- 🧠 **Smart Routing**: Automatically detects if the input is a math problem or a general query.  
- 💬 **Streamlit UI**: Interactive frontend with real-time chat and response view.

---

## 📸 Demo Screenshots

### Math Workflow  
![Math Flow](screenshots/Screenshot%202025-07-26%20232919.png)

### LLM Response Workflow  
![LLM Flow](screenshots/Screenshot%202025-07-26%20233026.png)

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/langgraph-agent.git
cd langgraph-agent
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Add Environment Variables
Create a .env file in the root directory with your Gemini or Google API key:

env
Copy
Edit
GEMINI_API_KEY=your_api_key_here
4. Run the App
bash
Copy
Edit
streamlit run main.py
✍️ Example Prompts
Input	Agent Action
What is 7 times 8?	Uses multiply tool
What is 15 + 7?	Uses plus tool
Tell me about Python	Routes to Gemini LLM
What is 5 plus?	Returns clarification

📦 Requirements
Python 3.10+

Streamlit

LangGraph

Google Generative AI SDK

python-dotenv

