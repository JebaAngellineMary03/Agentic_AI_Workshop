import streamlit as st
from langchain.agents import tool, create_tool_calling_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
import requests
import os
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

# Set API keys from environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# STEP 1: LLM Setup (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# STEP 2: Custom DuckDuckGo Wrapper
duckduckgo_tool = DuckDuckGoSearchRun()

@tool
def get_attractions(city: str) -> str:
    """Returns top 5-7 tourist places in the given city."""
    query = f"Top 7 tourist places to visit in {city}"
    return duckduckgo_tool.run(query)


@tool
def get_weather(city: str) -> str:
    """Fetches the current weather information for a given city using WeatherAPI."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        location = data['location']['name']
        condition = data['current']['condition']['text']
        temp_c = data['current']['temp_c']
        feelslike_c = data['current']['feelslike_c']
        time_observed = data['location']['localtime']
        return f"As of {time_observed}, the weather in {location} is {condition} with a temperature of {temp_c} °C (Feels like {feelslike_c} °C)."
    else:
        return f"Failed to fetch weather data for {city}. Please check the city name."

# STEP 4: Create Tools
tools = [get_weather, get_attractions]

# STEP 5: Create Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful multilingual travel assistant that provides:\n"
               "1. Weather report with time.\n"
               "2. Bullet list of 5-7 tourist attractions with emojis.\n"
               "3. A Google Maps link if available.\n"
               "4. A brief local language summary."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# STEP 6: Create Agent & Executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# STEP 7: Streamlit UI
st.set_page_config(page_title="Travel Assistant AI")
st.title("🌍 Intelligent Travel Assistant")
st.markdown("Enter your destination city to get weather info and top attractions.")

city = st.text_input("Destination City")

if st.button("Get Travel Info"):
    if city:
        user_input = f"Give me the weather and top attractions in {city}."
        result = agent_executor.invoke({"input": user_input})
        st.subheader("Travel Assistant Response")
        st.markdown(result["output"])
    else:
        st.warning("Please enter a city name.")
