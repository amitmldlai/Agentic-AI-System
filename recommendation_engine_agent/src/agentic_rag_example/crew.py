import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.weaviate_vector_search_tool import WeaviateVectorSearchTool
from crewai_tools import EXASearchTool
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


weaviate_vector_search_tool = WeaviateVectorSearchTool(
    weaviate_cluster_url=os.getenv("WEAVIATE_URL"),
    weaviate_api_key=os.getenv("WEAVIATE_API_KEY"),
    collection_name="netflix_data",
    limit=10,
)
exa_search_tool = EXASearchTool(api_key=os.getenv("EXA_API_KEY"))

llm = LLM(
    model="gpt-4",
    temperature=0.8,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
    api_key=os.getenv("OPENAI_API")
)


@CrewBase
class RecommendationEngineAgent:
    """AgenticRagExample crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def recommendation_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recommendation_generation_agent"],
            verbose=True,
            tools=[weaviate_vector_search_tool],
            llm=llm
        )

    @agent
    def recommendation_expansion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recommendation_expansion_agent"],
            verbose=True,
            tools=[exa_search_tool],
            llm=llm
        )

    @agent
    def recommendation_report_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recommendation_report_agent"],
            verbose=True,
            llm=llm
        )

    @task
    def recommendation_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["recommendation_generation_task"],
        )

    @task
    def recommendation_expansion_task(self) -> Task:
        return Task(
            config=self.tasks_config["recommendation_expansion_task"],
            # output_file="report.md"
        )

    @task
    def recommendation_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["recommendation_report_task"],
            output_file="report.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticRagExample crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
