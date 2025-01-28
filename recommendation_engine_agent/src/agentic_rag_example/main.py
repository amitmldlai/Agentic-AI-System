import warnings
from crew import RecommendationEngineAgent
from dotenv import load_dotenv

load_dotenv()


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {"query": "Find me Indian shows"}
    RecommendationEngineAgent().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
