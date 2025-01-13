from crewai import Agent
from crewai import LLM
from tools_setup import pdf_search_tool, EmailSenderTool
import os

# Basic configuration
llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.7, api_key=os.getenv("GOOGLE_API_KEY"))

research_agent = Agent(
    role="Research Agent",
    goal="Search through the PDF to find relevant answers",
    allow_delegation=False,
    verbose=True,
    backstory=(
        """
        The research agent is adept at searching and 
        extracting data from documents, ensuring accurate and prompt responses.
        """
    ),
    tools=[pdf_search_tool],
    llm=llm

)

professional_writer_agent = Agent(
    role="Professional Writer",
    goal="Write and send professional emails based on the research agent's findings",
    allow_delegation=False,
    verbose=True,
    backstory=(
        """
        The professional writer agent has excellent writing skills and is able to craft 
        clear and concise emails based on the provided information.
        """
    ),
    tools=[EmailSenderTool()],
    llm=llm
)