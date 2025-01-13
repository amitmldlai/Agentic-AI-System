from crewai import Task
from crewai_tools import FirecrawlSearchTool, RagTool
from tools.AddVideoToVectorDBTool import AddVideoToVectorDBTool
from tools.FetchLatestVideosFromYouTubeChannelTool import FetchLatestVideosFromYouTubeChannelTool
from agents_setup import scrape_agent, vector_db_agent, general_research_agent, follow_up_agent, fallback_agent
from pydantic_object import ContentCreatorInfo


fetch_latest_videos_tool = FetchLatestVideosFromYouTubeChannelTool()
add_video_to_vector_db_tool = AddVideoToVectorDBTool()
fire_crawl_search_tool = FirecrawlSearchTool()
rag_tool = RagTool()


scrape_youtube_channel_task = Task(
    description=(
        """
        Scrape the latest five videos from the specified YouTube channel.
        Extract relevant information about the content of the latest five videos.
        Ensure that all information comes directly from the YouTube channel and videos. 
        Do not make up any information.

        Here is the YouTube channel handle:

        {youtube_channel_handle}
        """
    ),
    expected_output="""
        Extract relevant information about the content of the latest five videos 
        from the specified YouTube channel.
        """,
    tools=[fetch_latest_videos_tool],
    agent=scrape_agent,
)

process_videos_task = Task(
    description=(
        """
        Process the extracted video urls from the previous task 
        and add them to the vector database.
        Ensure that each video is properly added to the vector database.
        All information must come directly from the searches. 
        Do not make up any information.

        """
    ),
    expected_output="""
        Successfully add the videos to the vector database.
        """,
    tools=[add_video_to_vector_db_tool],
    agent=vector_db_agent,
)

find_initial_information_task = Task(
    description=(
        """
        Ensure to fill out the `ContentCreatorInfo` model with 
        as much information as possible.

        ```
        class ContentCreatorInfo(BaseModel):
            first_name: Optional[str]
            last_name: Optional[str]
            main_topics_covered: Optional[List[str]]
            bio: Optional[str]
            email_address: Optional[str]
            linkedin_url: Optional[str]
            has_linked_in: Optional[bool] # if the user mentions they have a LinkedIn account, this is True
            x_url: Optional[str] 
            has_twitter: Optional[bool] # if the user mentions they have a Twitter account, this is True
        ```

        If any information is missing, leave the value as None.
        All information must come directly from the searches. 
        Do not make up any information.
        Rephrase and re-query as necessary to obtain all needed information.

        If looking for information as a whole doesn't work, 
            look for each item individually.
        When looking for a first name individually, search for phrases like, 
            "my name is", "hey guys, it's", 
            and other phrases a person would use to introduce themselves.
        When looking for an email, search for phrases like, 
            "you can contact me at", "my email is".
        """
    ),
    expected_output="""
        Fill out the `ContentCreatorInfo` model with as much information as possible. 
        Ensure all information is accurate and comes from the searches. 
        If any information is not found, leave it as None.
        """,
    tools=[rag_tool],
    agent=general_research_agent,
    output_pydantic=ContentCreatorInfo,
)

follow_up_task = Task(
    description=(
        """
        Search for any missing data in the `ContentCreatorInfo` model.
        Perform additional searches in the vector database to ensure completeness.
        All information must come directly from the searches. 
        Do not make up any information.
        Be thorough and creative in your search for missing data.

        If looking for information as a whole doesn't work, 
            look for each item individually.
        When looking for a first name individually, search for phrases like, 
            "my name is", "hey guys, it's", and other phrases a person would use 
            to introduce themselves.
        When looking for an email, search for phrases like, 
            "you can contact me at", "my email is".
        """
    ),
    expected_output="""
        Complete any missing fields in the `ContentCreatorInfo` model. 
        Ensure all information is accurate and comes from the searches.
        """,
    tools=[rag_tool],
    agent=follow_up_agent,
    output_pydantic=ContentCreatorInfo,
)

fallback_task = Task(
    description=(
        """
        Perform a final check and use web scraping to 
        find any remaining missing information on the 
        youtube channel with the following handle: 

        {youtube_channel_handle}

        Ensure the `ContentCreatorInfo` model is fully populated.
        All information must come directly from the searches. 
        Do not make up any information.
        """
    ),
    expected_output="""
        Ensure the `ContentCreatorInfo` model is fully populated. 
        Ensure all information is accurate and comes from the searches.
        """,
    tools=[fire_crawl_search_tool],
    agent=fallback_agent,
    output_pydantic=ContentCreatorInfo,
)
