import streamlit as st
from agents import ContentCreatorAgent, ContentCriticAgent

st.set_page_config(page_title="Smart Content Creation (Agentic Pattern)", layout="wide")
st.title("🧠 Smart Content Creation: Reflection-Based Agentic Pattern")
st.markdown("This app simulates a two-agent conversation for content creation and critique on **Agentic AI** using Gemini LLM.")

turns = st.number_input("Number of turns (3-5 recommended)", min_value=3, max_value=5, value=3)

class AgentExecutor:
    def __init__(self, topic, turns):
        self.topic = topic
        self.turns = turns
        self.creator = ContentCreatorAgent()
        self.critic = ContentCriticAgent()
        self.history = []

    def run(self):
        # Initial draft
        content = self.creator.run(self.topic)
        self.history.append(("Content Creator Agent (Initial Draft)", content))
        last_content = content
        for i in range(1, self.turns):
            feedback = self.critic.run(last_content)
            self.history.append((f"Content Critic Agent (Turn {i} Feedback)", feedback))
            revised = self.creator.run(self.topic, previous_content=last_content, feedback=feedback)
            self.history.append((f"Content Creator Agent (Turn {i} Revision)", revised))
            last_content = revised
        return last_content, self.history

if st.button("Simulate Conversation"):
    executor = AgentExecutor(topic="Agentic AI", turns=turns)
    final_content, history = executor.run()
    for role, text in history:
        if "Critic" in role:
            st.markdown(f"**{role}:**")
            st.warning(text)
        else:
            st.markdown(f"**{role}:**")
            st.info(text)
    st.markdown("---")
    st.subheader("Final Refined Content (Markdown)")
    st.markdown(final_content) 