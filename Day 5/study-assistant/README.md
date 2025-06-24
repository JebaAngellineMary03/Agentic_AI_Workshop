# 📚 Study Assistant – LangChain + Gemini Flash + Streamlit

This is a lightweight AI-powered **Study Assistant** that allows students to upload a PDF and instantly receive:

✅ A **concise summary**  
✅ **Multiple-choice quiz questions** for self-assessment

Built using **LangChain**, **Gemini 1.5 Flash**, and **Streamlit** — no vector databases or external storage required!

---

## 🚀 Features

- 📄 **PDF Upload**: Accepts any educational content in PDF format  
- ✨ **Summarization**: Uses Gemini to extract key points as bullet summary  
- 🧠 **Quiz Generation**: Creates 3 MCQs with 4 options and the correct answer  
- ⚡ **Fast & Lightweight**: Powered by Gemini 1.5 Flash via Google Generative AI  
- 🖥️ **Interactive UI**: Built with Streamlit for easy browser use

---

## 🧪 Tech Stack

- [LangChain](https://www.langchain.com/)
- [Gemini 1.5 Flash](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)

---

## 📂 Folder Structure

study-assistant/
├── app.py 
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/your-username/study-assistant.git
cd study-assistant
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Add Your Gemini API Key
You can generate a key at makersuite.google.com

Edit app.py or input it in the sidebar during runtime.

▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📸 Output Preview
🔑 Sidebar input for your Gemini API Key

📄 Upload a course PDF

📝 Get a summary and MCQs directly in the browser

✅ Sample Output
Summary:

Prompt Engineering is the design of prompts to control LLMs

Parameters like temperature and top-p affect output style

Examples include summarization, Q&A, classification, reasoning

Quiz Question Example:

Q: What is the purpose of low temperature in LLMs?
a) Random results
b) Precise answers
✅ Answer: c) Repetitive and focused outputs