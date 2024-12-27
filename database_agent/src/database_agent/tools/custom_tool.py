from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from crewai_tools import tool
import os
from crewai import LLM
from pathlib import Path


llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0
)

path = Path(__file__).parent.parent.parent.parent
database_path = os.path.join(path, "data", "salaries.db")
db = SQLDatabase.from_uri(f"sqlite:///{database_path}")


@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    list_tool = ListSQLDatabaseTool(db=db)
    return list_tool.invoke("")


@tool("tables_schema")
def tables_schema(table: str) -> str:
    """
    Input is a comma-separated list of table from list_tables tool, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling `list_tables` first!
    """
    info_tool = InfoSQLDatabaseTool(db=db)
    return info_tool.invoke(table)


@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result"""
    query_tool = QuerySQLDataBaseTool(db=db)
    return query_tool.invoke(sql_query)


@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    query_check = QuerySQLCheckerTool(db=db, llm=llm)
    return query_check.invoke({"query": sql_query})