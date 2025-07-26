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

![RAG Test Case](screenshots/Screenshot%202025-07-27%20003321.png)

---

### 2. 🤖 LLM Route – Direct LLM Response

**Query:** `What are the main components of a RAG model and how do they interact?`  
If no relevant documents exist, it falls back to Gemini Pro LLM.

![LLM Test Case](screenshots/Screenshot%202025-07-27%20004818.png)

---

### 3. 🌐 Web Search Route – Real-time Retrieval

**Query:** `What are the latest breakthroughs in quantum computing as of 2025?`  
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

<pre>
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
</pre>


---

## 🔧 Environment Setup

### 1.Install dependencies
<pre>pip install -r requirements.txt</pre>

### 2.Set environment variablesCreate a .env file in the root directory with the following:

.env
<pre>GEMINI_API_KEY=your_google_gemini_key</pre>

### 3.Run the app
<pre>python main.py</pre>
