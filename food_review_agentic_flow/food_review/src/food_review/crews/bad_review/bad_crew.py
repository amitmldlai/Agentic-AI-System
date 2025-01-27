from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from food_review.src.food_review.tools.custom_tool import DatabaseLoggerTool


@CrewBase
class BadFeedBackCrew:
    """BadFeedBack Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def negative_feedback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["negative_feedback_agent"],
        )

    @agent
    def db_update_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["db_update_agent"],
        )

    @task
    def handle_negative_feedback_tasks(self) -> Task:
        return Task(
            config=self.tasks_config["handle_negative_feedback_tasks"],
        )

    @task
    def update_db_tasks(self) -> Task:
        return Task(
            config=self.tasks_config["update_db_tasks"],
            tools=[DatabaseLoggerTool()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Crew that updates the DB when the feedback is negative"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )