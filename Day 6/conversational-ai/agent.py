import os
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from tools import search_competitors
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI( model="models/gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.3)

tools = [
    Tool(
        name="SearchCompetitors",
        func=search_competitors,
        description="Search for top clothing stores and footfall trends in a location"
    )
]

agent_executor: AgentExecutor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)
