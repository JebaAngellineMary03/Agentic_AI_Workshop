# 📄 PDF Research Agent

A multi-agent research assistant built using **LangChain**, **Streamlit**, and **Tavily API** that analyzes research paper PDFs. This tool extracts metadata, verifies authorship, estimates impact, and benchmarks the paper's novelty by comparing it with similar papers online.

---

## 🚀 Features

### 🧾 Metadata Extractor
Extracts:
- Title, Abstract, Keywords
- Authors and Authorship positions
- Journal/Conference name, DOI, Year

### ✍️ Authorship Verifier
Evaluates:
- Contribution quality
- Author position and significance
- Provides a verdict and checklist-style feedback

### 📈 Impact Estimator
Estimates:
- Technical depth and innovation
- Practical and academic value

### 📊 Research Benchmarking (RAG)
Benchmarks:
- Originality and relevance
- Compares your abstract with top 3 similar research papers
- Provides a 2–3 line summary and % similarity insight

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pdf-research-agent.git
cd pdf-research-agent

2. Create a Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
TAVILY_API_KEY=your_tavily_api_key_here
Ensure llm_config.py contains a valid LLM configuration (Google Gemini, OpenAI, etc.) exposed as llm.

▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📁 Project Structure
bash
Copy
Edit
.
├── app.py
├── llm_config.py
├── .env
├── tools/
│   ├── metadata_extractor.py
│   ├── authorship_verifier.py
│   ├── impact_estimator.py
│   └── benchmarking_agent.py
├── utils/
│   ├── pdf_utils.py
│   └── parser_utils.py
└── requirements.txt
📌 Requirements
Python 3.8+

Streamlit

Tavily SDK

LangChain-compatible LLM (OpenAI, Gemini, etc.)

