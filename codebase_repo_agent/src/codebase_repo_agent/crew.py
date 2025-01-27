import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .types_object import WebServer, DatabaseOutput, ORMOutput, APIOutput, APIDBTableOutput
from .utils import llm_mapping
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


llm_model = llm_mapping()
llm = llm_model["gemini"]
cwd = os.getcwd()


@CrewBase
class GitHubCrew:
    """GitHub Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        from .tools.custom_tool import tools, llama_tool, fallback_tool
        self.tool = tools()
        self.fallback_tool = llama_tool(os.path.join(cwd, "repo", st.session_state.repo_path))
        # self.fallback_tool = fallback_tool(os.path.join(cwd, "repo", st.session_state.repo_path))
        self.responses_dir = os.path.join(cwd, "responses", st.session_state.repo_path)

    @agent
    def github_webserver_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_webserver_agent"],
            # tools=[GithubSearchTool(gh_token=os.getenv("GITHUB_TOKEN"), content_types=["HTTP server", "web framework"])],
            tools=self.tool,
            # allow_delegation=True,
            llm=llm
            )

    @agent
    def github_database_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_database_agent"],
            tools=self.tool,
            # allow_delegation=True,
            llm=llm
            )

    @agent
    def github_orm_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_orm_agent"],
            tools=self.tool,
            # allow_delegation=True,
            llm=llm
        )

    @agent
    def github_api_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_api_agent"],
            tools=self.tool,
            # allow_delegation=True,
            llm=llm
        )

    @agent
    def github_api_databases_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_api_databases_agent"],
            tools=self.tool,
            # allow_delegation=True,
            llm=llm
        )

    @agent
    def github_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_summary_agent"],
            # allow_delegation=True,
            tools=self.tool,
            llm=llm
        )

    @agent
    def github_fallback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["github_fallback_agent"],
            # allow_delegation=True,
            tools=self.fallback_tool,
            llm=llm
        )

    @task
    def github_webserver_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_webserver_task"],
            async_execution=True,
            output_pydantic=WebServer,
            output_file=os.path.join(self.responses_dir, "webserver.json")
        )

    @task
    def github_database_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_database_task"],
            async_execution=True,
            output_pydantic=DatabaseOutput,
            output_file=os.path.join(self.responses_dir, "database.json"),
        )

    @task
    def github_orm_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_orm_task"],
            async_execution=True,
            output_pydantic=ORMOutput,
            output_file=os.path.join(self.responses_dir, "orm.json"),
        )

    @task
    def github_api_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_api_task"],
            async_execution=True,
            output_pydantic=APIOutput,
            output_file=os.path.join(self.responses_dir, "api.json"),
        )

    @task
    def github_api_databases_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_api_databases_task"],
            output_pydantic=APIDBTableOutput,
            output_file=os.path.join(self.responses_dir, "api_databases.json"),
        )

    @task
    def github_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_summary_task"],
            output_file=os.path.join(self.responses_dir, "summary.md"),
        )

    @task
    def github_fallback_task(self) -> Task:
        return Task(
            config=self.tasks_config["github_fallback_task"],
            output_file=os.path.join(self.responses_dir, "summary2.md"),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GitHub Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # manager_llm=llm_model["openai"],
            # manager_agent=self.github_codebase_manager
        )