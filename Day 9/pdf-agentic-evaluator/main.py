from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from tools.metadata_extractor import metadata_tool
from tools.authorship_verifier import authorship_tool
from tools.impact_estimator import impact_tool
from tools.research_benchmark import benchmarking_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

tools = [
    metadata_tool,
    authorship_tool,
    impact_tool,
    benchmarking_tool
]

agent_executor = initialize_agent(
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    llm=llm,
)

if __name__ == "__main__":
    query = "Evaluate the uploaded PDF file 'paper.pdf' under OKR Publish Research."
    result = agent_executor.run(query)
    print("\n✅ Final Gemini Evaluation:\n")
    print(result)
