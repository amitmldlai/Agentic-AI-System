import warnings
from crew import PdfRag
import os
from dotenv import load_dotenv
import agentops

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    question = input("What's your query?\n")
    inputs = {
        'query': question
    }

    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

    PdfRag().crew().kickoff(inputs=inputs)
    agentops.end_session()


if __name__ == '__main__':
    run()
