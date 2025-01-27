# from typing import Type
# from crewai.tools import BaseTool
# from pydantic import BaseModel
import streamlit as st
from crewai_tools import GithubSearchTool, DirectoryReadTool, FileReadTool
from crewai_tools import DirectorySearchTool
from llama_index.core import SimpleDirectoryReader
from llama_index.core import load_index_from_storage, StorageContext
from crewai_tools import LlamaIndexTool
from llama_index.core import VectorStoreIndex
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
# from codebase_repo_agent.src.codebase_repo_agent.types_object import WebServer, DatabaseOutput

load_dotenv()
cwd = os.getcwd()
print(cwd)


def tools():
    print('*'*50)
    print("Inside tool", os.path.join(cwd, "repo", st.session_state.repo_path))
    print('*' * 50)
    codebase_repo = os.path.join(cwd, "repo", st.session_state.repo_path)
    docs_tool = DirectoryReadTool(directory=codebase_repo)
    file_tool = FileReadTool()
    return [docs_tool, file_tool]


# Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
# Settings.llm = Gemini(model="models/gemini-1.5-flash", )
# Settings.embed_model = GeminiEmbedding(model_name='models/embedding-001')


def vector_query_index(codebase_dir):
    if not os.path.exists(os.path.join(cwd, 'index_storage')):
        parser = LlamaParse(result_type="markdown")

        file_extractor = {"code": parser}
        print("Inside fallback_tool", codebase_dir)
        documents = SimpleDirectoryReader(input_dir=codebase_dir,
                                          file_extractor=file_extractor,
                                          # input_files=['E:/Amit_github/github_agent/repo/Basic/initialize_db.py',
                                          #              'E:/Amit_github/github_agent/repo/Basic/main.py'],
                                          recursive=True).load_data()
        vector_store_index = VectorStoreIndex.from_documents(documents)
        vector_store_index.storage_context.persist(persist_dir=os.path.join(cwd, "indexes", st.session_state.repo_path, 'index_storage'))
    else:
        storage_context = StorageContext.from_defaults(persist_dir=os.path.join(cwd, "indexes", st.session_state.repo_path, 'index_storage'))
        vector_store_index = load_index_from_storage(storage_context)
    return vector_store_index


def llama_tool(codebase_dir):
    index = vector_query_index(codebase_dir)
    query_engine = index.as_query_engine(llm=OpenAI(model="gpt-4o", temperature=0.0))
    query_tool = LlamaIndexTool.from_query_engine(
        query_engine,
        name="Repository Codebase Tool",
        description="Use this tool to do analysis on codebase files",
        llm=OpenAI(model="gpt-4o", temperature=0.0)
    )

    return [query_tool]


def fallback_tool(codebase_dir):
    print("Inside fallback_tool", codebase_dir)
    directory_search = DirectorySearchTool(directory_path=codebase_dir)
    return [directory_search]