# 🌍 Intelligent Travel Assistant AI

This project is an interactive AI-based travel assistant built using **LangChain**, **Google Gemini API**, **DuckDuckGo Search**, and **WeatherAPI**. It provides users with:

- Real-time **weather information** of any city
- A **bullet list of top tourist attractions**
- Emojis, Google Maps links, and multilingual output
- A simple **Streamlit web interface**

---

## 🚀 Features

✅ Fetches live weather with date & time  
✅ Lists 5–7 top tourist attractions (uses DuckDuckGo)  
✅ Auto-formats output with emojis and maps  
✅ Provides multilingual summaries (if supported by LLM)  
✅ User-friendly via a Streamlit frontend

---

## 🛠️ Tech Stack

- **LangChain** – Tool handling & LLM agent execution  
- **Google Gemini (via LangChain)** – LLM for prompt reasoning  
- **DuckDuckGoSearch** – No-API web search for attractions  
- **WeatherAPI** – Real-time weather via HTTP request  
- **Streamlit** – Web app UI

---

## 📦 Installation

1. **Clone the repository**:

   <pre>git clone https://github.com/yourusername/travel-assistant-ai.git
   cd travel-assistant-ai </pre>

2. **Install dependencies**:

<pre> pip install -r requirements.txt</pre>

3. **Add your API keys**:

Get a Gemini API Key from https://makersuite.google.com/app/apikey

Get a WeatherAPI key from https://www.weatherapi.com 

## 🔑 Environment Setup
Update your .env or Python script with:

<pre>export GOOGLE_API_KEY="your_gemini_api_key"
export WEATHER_API_KEY="your_weather_api_key"</pre>

4. **▶️ Running the App**
   
<pre>streamlit run app.py
Then open the browser link shown (usually http://localhost:8501).</pre>

## 🧠 How It Works

The user inputs a city name.

### The agent:

-Calls a custom weather tool (via WeatherAPI)

-Calls a DuckDuckGo-based search tool for attractions

-The Gemini LLM formats the results into a natural, readable, and often multilingual response

-The result is shown in the Streamlit UI.

### 📷 Screenshot
<img width="1512" alt="Screenshot 2025-06-24 at 7 07 06 PM" src="https://github.com/user-attachments/assets/52380f3f-ac75-4b77-8467-3f8db1b83ecf" />


### ✨ Example Output

<pre>As of 2025-06-24 18:55, the weather in Coimbatore is Partly cloudy with a temperature of 28.3 °C (Feels like 32.0 °C).

Top Attractions:
• 🛕 Marudamalai Temple  
• 🌊 Noyyal River  
• 🏛️ Gass Forest Museum  
• 🛍️ Brookefields Mall  
• 🦚 TNAU Botanical Garden

📍 [View on Google Maps](https://www.google.com/maps/place/Coimbatore)

தமிழில்:
கோயம்புத்தூர் ஒரு அழகான நகரமாகும். மருதமலை கோவில் மிகவும் பிரபலமானது. </pre>
