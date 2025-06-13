# 🧠 AI Research Assistant – RAG-based QA on Academic PDFs

This project is an AI-powered **Question Answering System** built using the **Retrieval-Augmented Generation (RAG)** approach. It allows you to preload academic PDFs, ask questions about them, and get precise, source-cited answers using OpenAI and FAISS vector search.

---

## 🚀 Features

- 🔍 **Ask questions** from academic PDFs
- 📄 Preload custom pdfs in bulk
- 🧠 Uses **LangChain** chunking and **SBERT** for embedding
- ⚡ **FAISS** for efficient similarity search
- 🤖 Uses OpenAI GPT (gpt-4o-mini) to generate answers
- 🌐 Deployable via **Streamlit** 

---

## 🧪 Example Usage
Upload a research paper PDF or use preloaded documents, then ask questions like:

❓ "What is the architecture of the RAG model?"
❓ "What are the results of the ablation study?"

You’ll get an answer like:

✅ “The RAG model consists of a retriever and a generator [2].”

## 📁 Project Structure

```bash
.
├── app.py                     # Streamlit frontend
├── preload_documents.py       # Preprocess and preload PDFs into FAISS
├── answer_generator.py        # Generates answers using OpenAI API
├── src/
│   ├── loader.py              # Loads PDFs and extracts text
│   ├── chunker.py             # Splits documents into manageable chunks
│   ├── vectorizer.py          # Embeds chunks using SentenceTransformer
│   ├── retriever.py           # Builds and loads FAISS index
│   └── query_engine.py        # Combines retrieval + generation logic
├── vector_store/              # Saved FAISS index
└── data/
    └── papers/                # PDF files to preload

⚙️ Setup Instructions
Clone the repo

bash
Copy code
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
Create and activate virtual environment

bash
Copy code
python -m venv .venv
source .venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set your OpenAI key
Create a .env file:

env
Copy code
OPENAI_API_KEY=your_openai_key
(Optional) Preload PDFs
Place PDFs inside data/papers/, then run:

bash
Copy code
python preprocess.py
Run the app

bash
Copy code
streamlit run app.py
