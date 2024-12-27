import warnings
from crew import DatabaseAgent
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        "query": "What is the average pay of Data Scientist"
    }

    DatabaseAgent().crew().kickoff(inputs=inputs)


run()