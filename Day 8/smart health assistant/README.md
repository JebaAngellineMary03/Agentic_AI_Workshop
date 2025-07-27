# 🤖 Smart Health Assistant (Sequential Multi-Agent System)

A Streamlit-based health planner that uses a chain of AI agents (powered by Google Gemini) to generate a personalized health plan—including BMI analysis, diet, and workout schedule—based on user input.

---

## 🧩 Agents and Workflow

1. **User Proxy Agent**: Collects user data (weight, height, age, gender, dietary preference)
2. **BMI Tool & Agent**: Calculates BMI and provides health recommendations
3. **Diet Planner Agent**: Suggests a meal plan based on BMI and dietary preference
4. **Workout Scheduler Agent**: Creates a weekly workout plan based on age, gender, and meal plan

All reasoning and plan generation is handled by Google Gemini LLM.

---

## 🚀 Features

- Sequential multi-agent conversation (User → BMI → Diet → Workout)
- Streamlit web interface for easy input/output
- Gemini LLM for all agent reasoning
- Final output: Complete health plan with BMI insights, tailored diet, and fitness schedule

---

## 🖥️ UI Screenshots

| Input Form | BMI & Diet Output | Workout Plan | Full Plan |
|------------|-------------------|--------------|-----------|
| ![Form](screenshots/Screenshot%202025-07-27%20180911.png) | ![BMI & Diet](screenshots/Screenshot%202025-07-27%20180936.png) | ![Workout](screenshots/Screenshot%202025-07-27%20180949.png) | ![Full Plan](screenshots/Screenshot%202025-07-27%20181005.png) |

---

## 🛠️ Setup & Usage

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/smart-health-assistant.git
   cd "Day 8/smart health assistant"
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key**
   - Edit `agents.py` and replace the placeholder with your own Google Gemini API key.

4. **Run the app**
   ```sh
   streamlit run app.py
   ```

---

## 📁 Project Structure

- `app.py` — Streamlit UI and agent orchestration
- `agents.py` — All agent classes and Gemini integration
- `requirements.txt` — Python dependencies
- `screenshots/` — Example UI outputs

---

