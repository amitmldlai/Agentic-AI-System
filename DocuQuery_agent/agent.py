from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
import os
from knowledge_base import create_knowledge_base

os.makedirs("db", exist_ok=True)
os.makedirs("reports", exist_ok=True)

knowledge_base = create_knowledge_base()

query_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Use tables to display data"],
    knowledge_base=knowledge_base,
    search_knowledge=True,
    storage=SqlAgentStorage(table_name="agent_app", db_file="db/agents.db"),
    add_history_to_messages=True,
    markdown=True,
    show_tool_calls=True,
    stream=True,
    save_response_to_file='reports/Report.md'
)

query_agent.print_response("Give the information about how memory and retrievers work in Agentic System")