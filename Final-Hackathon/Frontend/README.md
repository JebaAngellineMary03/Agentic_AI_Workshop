# 🎥 Video Pitch Evaluation Portal – Frontend

This is the frontend of the **Pitch Analysis AI Platform** built with **React** and **Tailwind CSS**. It enables users to:

- 📥 Submit YouTube video links for evaluation
- 📊 View scores for **content**, **clarity**, **tone**, and **structure**
- 📝 Read AI-generated feedback reports
- 🔍 Explore detailed insights via an interactive UI

---

## 🌐 Live Demo

https://drive.google.com/file/d/1-1pwA76UE8VjBazDRZ5T3wXsfT9gFAa8/view?usp=sharing

---

## 📁 Project Structure

<pre>Frontend/
├── public/
├── src/
│ ├── api/
│ │ └── api.js # Axios config and backend API calls
│ ├── components/
│ │ ├── ui/ # Reusable UI elements
│ │ │ ├── button.jsx
│ │ │ ├── card.jsx
│ │ │ ├── input.jsx
│ │ │ └── tabs.jsx
│ │ └── VideoDashboard.jsx # Main dashboard for evaluations
│ ├── App.js # App entry point with routing
│ ├── index.js # ReactDOM render
│ └── styles.css / index.css # Tailwind and global styles
├── postcss.config.js
├── tailwind.config.js
├── package.json
└── README.md
</pre>

---

## 🚀 Features

- **🎯 Dashboard:** Lists all evaluated video submissions.
- **📨 Video Input Form:** Lets users submit YouTube URLs.
- **📈 Coaching Popup:** Displays full feedback report and score breakdown in a modal.
- **🧩 Modular Components:** Built using clean reusable UI components.
- **🎨 Tailwind CSS:** Fast, responsive, and modern UI with a gradient background.

---

## 🛠️ Setup Instructions

1. **Clone the repository:**

<pre>git clone https://github.com/yourusername/pitch-evaluation-frontend.git
cd pitch-evaluation-frontend </pre>

2.**Install dependencies:**

<pre>npm install</pre>

3. **Start the development server:**

<pre>npm start
Ensure backend is running on http://localhost:8000 </pre>

## 📦 Dependencies
1.react
2.axios
3.react-markdown
4.tailwindcss
5.postcss
6.autoprefixer

