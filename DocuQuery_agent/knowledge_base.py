import os

from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.qdrant import Qdrant
from dotenv import load_dotenv

cwd = os.getcwd()
load_dotenv()
api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
collection_name = "agent_app"

vector_db = Qdrant(
    collection=collection_name,
    url=qdrant_url,
    api_key=api_key,
)


def create_knowledge_base():
    knowledge_base = PDFKnowledgeBase(
        path=os.path.join(cwd, "data"),
        vector_db=vector_db,
        reader=PDFReader(chunk=True)
    )
    if not vector_db.exists():
        knowledge_base.load()
    return knowledge_base

