from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class NeutralFeedbackCrew:
    """Crew for handling Neutral Feedback"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def neutral_feedback_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["neutral_feedback_agent"],
        )

    @task
    def handle_neutral_feedback_task(self) -> Task:
        return Task(
            config=self.tasks_config["handle_neutral_feedback_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates a Crew for handling Neutral Feedback and suggesting alternative restaurants"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
