# 🧠 Web Research Agent using Gemini + Tavily

This is a Streamlit-based research assistant that automates the generation of structured research reports using **Google Gemini (Generative AI)** and **Tavily Web Search API**.

It takes a topic as input, generates insightful questions, performs real-time web searches to gather information, summarizes the results using Gemini, and compiles everything into a downloadable report (Markdown or PDF).

---

## ✨ Features

- 🔎 **AI-generated research questions** on the entered topic  
- 🌐 **Web search using Tavily** for real-time data  
- ✍️ **Summarization with Gemini** (Google Generative AI)  
- 📝 **Auto-generated structured reports**  
- 📄 **Downloadable in Markdown and PDF formats**  
- ⚙️ Powered by `streamlit`, `reportlab`, and `dotenv`

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/web-research-agent.git
cd web-research-agent
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Create a .env file
ini
Copy
Edit
# .env
GEMINI_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
Note: Never share your API keys publicly. Do not commit the .env file.

4. Run the app
bash
Copy
Edit
streamlit run app.py
🖥️ Usage
Enter a research topic (e.g., Artificial Intelligence in Healthcare)

Click "Run Research Agent"

Wait for the agent to:

Generate questions

Search the web

Summarize findings

Compile the final report

Download the result in Markdown or PDF format

📁 Project Structure
bash
Copy
Edit
web-research-agent/
├── app.py                 # Main Streamlit app
├── .env                   # API keys (DO NOT COMMIT)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
📦 Dependencies
streamlit

google-generativeai

tavily-python

reportlab

python-dotenv

Install them with:

bash
Copy
Edit
pip install streamlit google-generativeai tavily-python reportlab python-dotenv
