# 📄 Research Paper Authorship Checker with RAG Similarity

A **Streamlit-based web app** to verify the **authenticity of research papers** using **Large Language Models (LLMs)** and **RAG (Retrieval-Augmented Generation)** techniques.

This tool helps you determine if sections of a research paper are **AI-generated** and checks the **originality** of the abstract by comparing it with similar published works.

---

## 🚀 Features

### ✅ Metadata Extraction  
Automatically extracts:
- Title  
- Authors  
- Abstract  
from uploaded PDF files using **PyMuPDF**.

### 📊 Citation Count Fetching  
Retrieves the citation count of the paper from [OpenAlex](https://openalex.org/).

### 🧠 Section-wise AI Detection  
Uses **Gemini Pro** to classify each section of the paper as:
- ✅ Human-written  
- ❌ AI-generated

### 🔍 Abstract Similarity Check (RAG)  
Fetches similar papers using OpenAlex and evaluates how closely the uploaded paper's abstract resembles them, returning a **similarity score (0–100)**.

---

## 🧰 Technologies Used

- **[Streamlit](https://streamlit.io/)** – Interactive UI  
- **[PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)** – PDF parsing and text extraction  
- **[Google Gemini API](https://ai.google.dev/)** – LLM for classification and similarity scoring  
- **[OpenAlex API](https://docs.openalex.org/)** – Academic research database  
- **Pandas** – Display tabular verdicts on section analysis  

---

## 📦 Installation
Install required packages using pip:

<pre> pip install streamlit pymupdf google-generativeai pandas requests </pre>

## 🔑 API Key Setup
You can store your API keys securely using a .env file or directly in your code:

<pre>GEMINI_API_KEY1 = "your-gemini-api-key-1"  # For section-wise classification  
GEMINI_API_KEY2 = "your-gemini-api-key-2"  # For abstract similarity scoring </pre>

## ▶️ Running the App

<pre>streamlit run app.py</pre>

## 🧪 How It Works
1.Upload a research paper (PDF).

2.**The app**:

-Extracts metadata: Title, Authors, Abstract

-Fetches citation count using OpenAlex

-Splits the full text into logical sections

-Uses Gemini to classify each section as AI-generated or Human-written

-Uses RAG (Gemini + OpenAlex) to check abstract similarity with related works

3.**Displays**: 
-Section-wise verdicts (✅ / ❌)
-Final similarity percentage

## 📸 Demo Screenshot
![image](https://github.com/user-attachments/assets/e31d5840-1c68-4e65-a09b-838d094a6cf2)
---
![image](https://github.com/user-attachments/assets/3fe50171-e27c-462b-9e1a-005349f1b360)
<h3 align="center">Example of Section Classification and Similarity Check</h3>

