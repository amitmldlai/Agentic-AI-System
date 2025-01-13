from crewai import Agent
from tools.AddVideoToVectorDBTool import AddVideoToVectorDBTool
from tools.FetchLatestVideosFromYouTubeChannelTool import FetchLatestVideosFromYouTubeChannelTool
from crewai_tools import FirecrawlSearchTool, RagTool
from crewai import LLM
import os

fetch_latest_videos_tool = FetchLatestVideosFromYouTubeChannelTool()
add_video_to_vector_db_tool = AddVideoToVectorDBTool()
fire_crawl_search_tool = FirecrawlSearchTool()
rag_tool = RagTool()

llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.7, api_key=os.getenv("GOOGLE_API_KEY"))

scrape_agent = Agent(
    role="Scrape Agent",
    goal="Scrape content from YouTube videos.",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        - A dedicated professional focused on extracting and processing content
            from YouTube videos.
        - You ensure that all video content is accurately scraped and added to 
            the vector database.
        - You are thorough and fact-driven, ensuring the highest quality of data.
        """
    ),
    tools=[fetch_latest_videos_tool],
    llm=llm,
)

vector_db_agent = Agent(
    role="Vector DB Processor",
    goal="Add YouTube videos to the vector database",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        A detail-oriented professional who ensures that video content 
        is accurately processed and added to the vector database.
        """
    ),
    tools=[add_video_to_vector_db_tool],
    llm=llm,
)

general_research_agent = Agent(
    role="General Research Agent",
    goal="Analyze the YouTube channel and gather all required information",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        An analytical professional adept at extracting 
        actionable information from various sources. 
        You are persistent and fact-driven, ensuring all gathered information 
        is accurate and derived from reliable sources. 
        You will rephrase and re-query as necessary to obtain all needed information.
        When looking for specific details, you will search for common phrases people use
        to introduce themselves or provide contact details.
        """
    ),
    tools=[rag_tool],
    llm=llm,
)

follow_up_agent = Agent(
    role="Follow-up Agent",
    goal="Perform follow-up research to find any missing data",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        A diligent researcher focused on thoroughness. 
        You are the last line of defense in ensuring completeness of the information. 
        You will be thorough and creative in your search for missing data, ensuring 
        that all gathered information is fact-driven and accurate.
        When looking for specific details, you will search for common phrases people use
        to introduce themselves or provide contact details.
        """
    ),
    tools=[rag_tool],
    llm=llm,
)

fallback_agent = Agent(
    role="Fallback Agent",
    goal="Perform final checks and search the internet for missing information",
    verbose=True,
    allow_delegation=False,
    backstory=(
        """
        A meticulous researcher with skills in deep web searches.

        If you hit a rate limit, sleep for the specified time then retry again.
        """
    ),
    tools=[fire_crawl_search_tool],
    llm=llm,
)