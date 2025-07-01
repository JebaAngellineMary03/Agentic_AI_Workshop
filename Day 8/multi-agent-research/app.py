import os
import faiss
import requests
import openai
from langgraph import LangGraph, Node
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Set up Gemini API key (assumed from your environment)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize OpenAI and Gemini API clients
openai.api_key = GEMINI_API_KEY
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Using Sentence-Transformers model for embeddings

# Define the Router Agent
def router_agent(query):
    if 'latest' in query.lower() or 'current' in query.lower():
        return "web_research"
    return "rag"

# Define the Web Research Agent
def web_research_agent(query):
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    return response.json()

# Define the RAG Agent
def rag_agent(query):
    # Simulate retrieval of information from a knowledge base (e.g., vector database)
    dataset = ["Artificial Intelligence", "Machine Learning", "Natural Language Processing"]
    response = [item for item in dataset if query.lower() in item.lower()]
    return response

# Define the Summarization Agent
def summarization_agent(information):
    # Use the Gemini API (or any LLM) for summarizing the collected information
    summary_prompt = f"Please summarize the following information: {information}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=summary_prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Set up LangGraph workflow
def create_langgraph_workflow():
    graph = LangGraph()
    start_node = Node("start")
    router_node = Node("router", function=router_agent)
    web_research_node = Node("web_research", function=web_research_agent)
    rag_node = Node("rag", function=rag_agent)
    summarization_node = Node("summarization", function=summarization_agent)

    # Define conditional edges
    graph.add_edge(start_node, router_node)
    graph.add_edge(router_node, web_research_node, condition=lambda result: result == "web_research")
    graph.add_edge(router_node, rag_node, condition=lambda result: result == "rag")
    graph.add_edge(web_research_node, summarization_node)
    graph.add_edge(rag_node, summarization_node)
    
    return graph

# Streamlit interface
def main():
    st.title("Multi-Agent Research and Summarization System")
    
    user_query = st.text_input("Enter your research query:")

    if user_query:
        # Initialize LangGraph workflow
        graph = create_langgraph_workflow()

        # Start the workflow
        result = graph.run(user_query)

        # Show results
        st.subheader("Research and Summary Output")
        st.write(result)

if __name__ == "__main__":
    main()
