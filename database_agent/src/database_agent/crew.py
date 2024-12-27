from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from pathlib import Path
from tools.custom_tool import list_tables, tables_schema, execute_sql, check_sql
from dotenv import load_dotenv


load_dotenv()
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
llm = ChatGroq(
    temperature=0,
    model="groq/llama-3.1-8b-instant"
)


@CrewBase
class DatabaseAgent:
    """DatabaseAgent crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def sql_dev(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_dev'],
            verbose=True,
            tools=[list_tables, tables_schema, execute_sql, check_sql],
            llm=llm
        )

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst'],
            verbose=True,
            llm=llm
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],
            llm=llm
        )

    @task
    def extract_data(self) -> Task:
        return Task(
            config=self.tasks_config['extract_data'],
        )

    @task
    def analyze_data(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_data'],
        )

    @task
    def write_report(self) -> Task:
        return Task(
            config=self.tasks_config['write_report'],
            output_file='query_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DatabaseAgent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            output_log_file="crew.log",

        )
