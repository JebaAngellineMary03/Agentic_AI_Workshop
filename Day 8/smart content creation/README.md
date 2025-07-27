# Smart Content Creation: Reflection-Based Agentic Pattern

This project simulates a two-agent conversation for content creation and critique on the topic of Agentic AI. It uses Streamlit for the UI and Google Gemini LLM for language generation and evaluation.

## Agents
- **Content Creator Agent:** Drafts content on Generative AI topics.
- **Content Critic Agent:** Evaluates drafts for language and technical accuracy, providing constructive feedback.

## Features
- Reflection-based agentic pattern (iterative feedback and revision)
- Up to 5 conversational turns
- Final content displayed in markdown
- Streamlit web interface
- Gemini LLM for all agent reasoning (API key in code)

## Usage
1. Install requirements: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`

## Example Screenshots

Below are example outputs from the Streamlit app:

### 1. App Home and Initial Draft
*The app interface and the Content Creator Agent's initial draft on Agentic AI.*
![App Home and Initial Draft](screenshots/Screenshot%202025-07-27%20173550.png)

### 2. Critic Feedback (Turn 1)
*The Content Critic Agent provides detailed feedback on the initial draft.*
![Critic Feedback (Turn 1)](screenshots/Screenshot%202025-07-27%20173614.png)

### 3. Creator Revision and Critic Feedback (Turn 2)
*The Content Creator Agent revises the draft, and the Critic Agent provides further feedback.*
![Creator Revision and Critic Feedback (Turn 2)](screenshots/Screenshot%202025-07-27%20173637.png)

### 4. Final Refined Content (Markdown)
*The final, refined markdown content after all agentic turns.*
![Final Refined Content (Markdown)](screenshots/Screenshot%202025-07-27%20173707.png)

--- 