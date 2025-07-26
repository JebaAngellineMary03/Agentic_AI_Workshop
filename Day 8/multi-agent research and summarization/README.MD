# 🧠 Multi-Agent Research Summarizer

A multi-agent app that intelligently chooses the best route—RAG, Web Search, or LLM—to summarize answers to complex research queries. Built with LangChain, Gemini Pro, FAISS, and FastAPI.

---

## 🚀 Features

- 🔍 **Input** a research question and get a summarized answer.
- 🧭 **Route Selector Agent**:
  - ✅ Uses **RAG** if relevant data exists in local FAISS index.
  - 🌐 Falls back to **Web Search** if local data is insufficient.
  - 🤖 Uses **LLM-only** if no RAG or web data is found.
- 📘 Displays the route taken and the final result.
- 📂 Modular architecture with agents for each route.
- 🖼️ Integrated with a `screenshots/` folder to visualize all flows.

---

## 🧪 Test Case Flows

### 1. ✅ RAG Route – Local Dataset

**Query:** `What is deep learning?`  
If your FAISS index contains relevant content, the RAG agent provides a precise answer.

![RAG Test Case](screenshots/Screenshot%202025-07-27%20004818.png)

---

### 2. 🤖 LLM Route – Direct LLM Response

**Query:** `Explain quantum entanglement in simple terms`  
If no relevant documents exist, it falls back to Gemini Pro LLM.

![LLM Test Case](screenshots/Screenshot%202025-07-27%20003321.png)

---

### 3. 🌐 Web Search Route – Real-time Retrieval

**Query:** `Latest trends in generative AI in 2025`  
No RAG matches, so the system performs a web search and summarizes the results.

![Web Research Test Case](screenshots/Screenshot%202025-07-27%20004924.png)

---

## 🛠️ Tech Stack

- 🧠 [LangGraph](https://www.langchain.com/langgraph)
- 🧩 [LangChain](https://www.langchain.com/)
- 📚 FAISS for vector search
- 🌐 Google Gemini API (LLM + Embeddings)
- 🖥️ FastAPI backend
- ⚡ React frontend (optional)
- 📸 Python + VS Code for automation

---

## 📂 Folder Structure

.
├── agents/
│ ├── rag_agent.py
│ ├── llm_agent.py
│ └── web_agent.py
├── faiss_index/
├── screenshots/
│ ├── rag_testcase.png
│ ├── llm_testcase.png
│ └── web_testcase.png
├── .env
├── main.py
├── README.md


---

## 🔧 Environment Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
Set environment variables
Create a .env file:

ini
Copy
Edit
GEMINI_API_KEY=your_google_gemini_key
SERPAPI_KEY=your_serpapi_key
Build FAISS index (optional, if not already done)

python
Copy
Edit
from langchain.vectorstores import FAISS
# Your FAISS creation code here
Run the app

bash
Copy
Edit
python main.py
🧠 Sample Queries to Try
"What is diffusion in AI?"

"Trends in LLM-based search engines in 2025"

"Applications of deep learning in education"