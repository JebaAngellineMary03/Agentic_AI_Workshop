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

<pre> study-assistant/
├── app.py 
├── requirements.txt # Python dependencies
└── README.md # Project documentation
</pre>

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

<pre>git clone https://github.com/your-username/study-assistant.git
cd study-assistant</pre>

### 2️⃣ Install Dependencies

<pre>pip install -r requirements.txt</pre>

### ▶️ Run the App

<pre>streamlit run app.py</pre>

## 📸 Output Preview
<img width="1512" alt="Screenshot 2025-06-24 at 6 08 07 PM" src="https://github.com/user-attachments/assets/6835cbf1-afd9-4757-89f6-b83de71f66ae" />

<img width="1512" alt="Screenshot 2025-06-24 at 6 08 15 PM" src="https://github.com/user-attachments/assets/5643e062-a323-4c2d-8381-101f2d92044c" />


## ✅ Sample Output

# Summary:

Prompt Engineering is the design of prompts to control LLMs

Parameters like temperature and top-p affect output style

Examples include summarization, Q&A, classification, reasoning

# Quiz Question Example:

Q: What is the purpose of low temperature in LLMs?
a) Random results
b) Precise answers
✅ Answer: c) Repetitive and focused outputs
