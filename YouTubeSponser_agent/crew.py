from dotenv import load_dotenv
from agents_setup import *
from tasks_setup import *

# Load environment variables
load_dotenv()


fetch_latest_videos_tool = FetchLatestVideosFromYouTubeChannelTool()
add_video_to_vector_db_tool = AddVideoToVectorDBTool()
fire_crawl_search_tool = FirecrawlSearchTool()
rag_tool = RagTool()


# --- Crew ---
crew = Crew(
    agents=[
        scrape_agent,
        vector_db_agent,
        general_research_agent,
        follow_up_agent,
        fallback_agent,
    ],
    tasks=[
        scrape_youtube_channel_task,
        process_videos_task,
        find_initial_information_task,
        follow_up_task,
        fallback_task,
    ],
    process=Process.sequential,
)

youtube_channel_handle = input("Please enter the YouTube handle to analyze:\n")
result = crew.kickoff(inputs={"youtube_channel_handle": youtube_channel_handle})
print(result)
