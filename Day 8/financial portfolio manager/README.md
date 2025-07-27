# Financial Portfolio Manager

A Streamlit-based agentic system to help users analyze and optimize their investment portfolios using Google Gemini LLM and a collaborative agent workflow.

## Features
- **Agent Collaboration:** Multiple specialized agents (Portfolio Analysis, Growth/Value Investment, Investment Advisor) collaborate via a group chat workflow.
- **Dynamic Workflow:** Uses StateFlow logic to route between growth and value investment strategies based on user profile.
- **Personalized Reports:** Generates a detailed, personalized financial report with actionable investment suggestions.
- **Modern UI:** Simple, interactive Streamlit interface.
- **Google Gemini LLM:** All analysis and recommendations are powered by Gemini (API key set directly in code).

## Folder Structure
```
financial portfolio manager/
├── agents.py                # All agent workflow logic
├── app.py                   # Streamlit UI
├── gemini_api.py            # Gemini API utility
├── requirements.txt         # Dependencies
├── screenshots/             # App screenshots
│   ├── Screenshot 2025-07-28 012625.png
│   ├── Screenshot 2025-07-28 012656.png
│   └── Screenshot 2025-07-28 012708.png
```

## Setup & Installation
1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **API Key:**
   - The Google Gemini API key is set directly in `gemini_api.py` (no .env file needed).
   - If you wish to use your own key, edit the `API_KEY` variable in `gemini_api.py`.

## Running the App
```sh
streamlit run app.py
```
- Open the provided local URL in your browser.
- Enter your salary and a summary of your current investments.
- Click **Analyze Portfolio** to generate your personalized report.

## Agent Workflow
1. **User Proxy Agent:** Initiates the workflow.
2. **Group Chat Manager:** Orchestrates agent collaboration.
3. **Portfolio Analysis Agent:** Analyzes user input and determines investment category (Growth/Value).
4. **StateFlow:** Routes to the appropriate investment agent.
5. **Growth/Value Investment Agent:** Provides tailored investment suggestions.
6. **Investment Advisor Agent:** Compiles and presents the final report.

## Screenshots
| Home Page | Financial report | Agent conversation log |
|-----------|--------------|---------------|
| ![Home](screenshots/Screenshot%202025-07-28%20012625.png) | ![Output 1](screenshots/Screenshot%202025-07-28%20012656.png) | ![Output 2](screenshots/Screenshot%202025-07-28%20012708.png) |

## Sample Input & Output
**Input:**
- Salary: 100000
- Portfolio: "50000 in fixed deposits, 20000 in SIPs, 30000 in real estate"

**Output:**
- A detailed financial report including:
  - Executive summary
  - Portfolio breakdown
  - Growth or value investment suggestions
  - Personalized recommendations
  - Current date

## Notes
- No .env file is used; API key is set directly in code.
- All agent logic is modularized in `agents.py`.
- For any issues, check your API key and internet connection.
