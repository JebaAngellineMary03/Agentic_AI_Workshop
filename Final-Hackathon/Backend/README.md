# 🎯 Pitch Analysis Backend

This backend system powers a **Video Pitch Evaluation Platform** that analyzes YouTube pitch videos and provides automated feedback. It uses a **multi-agent AI architecture**, integrates **LangGraph**, and provides structured feedback including clarity, tone, structure, and content quality.

---

## 🚀 Features

- 🔗 Analyze YouTube pitch videos
- 🧠 Multi-agent architecture (LangGraph + Agents)
- 📝 Returns structured score + markdown feedback
- 🧾 Stores evaluations in MongoDB
- 🔍 FAISS integration for fast retrieval
- 🌐 FastAPI-based clean RESTful API
- 📤 JSON input, Markdown feedback output

---

## 📡 API Endpoints

| Method | Endpoint              | Description                                  |
|--------|-----------------------|----------------------------------------------|
| POST   | `/analyze`            | Analyze a YouTube video                      |
| GET    | `/evaluations`        | Get all video evaluation summaries           |
| GET    | `/feedback_logs`      | Retrieve previous feedback by YouTube URL    |

---

## 📦 Backend Project structure/
<pre>
├── agents/
│ ├── init.py
│ ├── clarity_agent.py
│ ├── content_agent.py
│ ├── download_agent.py
│ ├── error_handler.py
│ ├── feedback_agent.py
│ ├── structure_agent.py
│ └── router.py
│
├── app/
│ ├── init.py
│ ├── api.py
│ ├── crud.py
│ ├── db.py
│ └── models.py
│
├── chains/
│ ├── metadata_chain.py
│ └── transcript_chain.py
│
├── core/
│ └── runner.py
│
├── data/
│ └── pitch_templates.json
│
├── faiss_index/
│ └── (index files)
│
├── graph/
│ └── graph.py
│
├── llms/
│ └── llms.py
│
├── prompts/
│ └── prompt_templates.py
│
├── state/
│ └── state.py
│
├── tools/
│ ├── clarity_tone_analysis_tool.py
│ ├── content_analysis_tool.py
│ ├── download_and_extract_tool.py
│ ├── generate_final_report_tool.py
│ ├── structure_analysis_tool.py
│
├── utils/
│ ├── faiss_utils.py
│ ├── youtube_utils.py
│ └── create_index.py
│
├── main.py
├── requirements.txt
└── .env
</pre>

## 🔐Environment Variables
<pre>MONGO_URI="mongodb://localhost:27017"
GOOGLE_API_KEY="your_google_api_key_here" </pre>

## ⚙️ Setup Instructions

# Clone the repository
<pre>git clone https://github.com/your-username/your-repo.git
cd Backend
</pre>

# Create a virtual environment
<pre>python -m venv .venv
source .venv/bin/activate</pre>

# Install dependencies
<pre> pip install -r requirements.txt </pre>

# Run the server
<pre> python main.py 
Your API will now be available at: http://localhost:8000 </pre>

## 📬 Sample Request

<pre> POST /analyze HTTP/1.1
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=wJfjDyAmy7U"
}
</pre>

## 🧠 Agent Workflow Overview
![agentsWorkflow drawio](https://github.com/user-attachments/assets/dafa519b-d624-43e1-84e0-67e9ad203c41)

## 📚 Tech Stack

# 1.Python 3.9+
# 2.FastAPI
# 3.LangGraph / LangChain
# 4.MongoDB
# 5.FAISS
# 6.Gemini
# 7.yt-dlp



