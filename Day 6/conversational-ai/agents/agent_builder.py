from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.business_tools import search_competitors_enhanced, generate_market_analysis, get_location_insights
import streamlit as st

def build_agent():
    api_key = "AIzaSyCvpeCpwNe1auSU0jh_w6JssnlWnHrMc0Y"
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.5
    )

    tools = [
        search_competitors_enhanced,
        generate_market_analysis,
        get_location_insights
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent
