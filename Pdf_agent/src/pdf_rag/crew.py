from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import PDFSearchTool
import os

cwd = os.getcwd()

load_dotenv()

pdf_search_tool = PDFSearchTool(pdf=os.path.join(cwd, "agentops.pdf"))


@CrewBase
class PdfRag:
    """PdfRag crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def pdf_rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_rag_agent'],
            tools=[pdf_search_tool],
            verbose=True
        )

    @agent
    def pdf_summary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_summary_agent'],
            verbose=True
        )

    @task
    def pdf_rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_rag_task'],
        )

    @task
    def pdf_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_summary_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PdfRag crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
