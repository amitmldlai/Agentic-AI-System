from typing import List, Optional
from pydantic import BaseModel, Field


class WebServer(BaseModel):
    name: str = Field(None, description="Name of the web server used in the codebase, if any.")
    is_present: bool = Field(False, description="Indicates whether the codebase contains a web server.")
    details: str = Field(False, description="Details about its implementation, such as entry points, initialization, and any key configurations.")


class Database(BaseModel):
    name: str = Field(..., description="Name of the database used in the codebase.")
    description: Optional[str] = Field(None, description="Additional details about the database configuration or usage.")


class DatabaseOutput(BaseModel):
    databases: List[Database] = Field(..., description="List of databases used in the codebase, along with their details.")


class ORM(BaseModel):
    name: str = Field(..., description="Name of the ORM (Object-Relational Mapping) framework used.")
    description: Optional[str] = Field(None, description="Additional details about the ORMs usage and configuration.")


class ORMOutput(BaseModel):
    orm: List[ORM] = Field(..., description="List of ORM frameworks used in the codebase, with their details.")


class API(BaseModel):
    endpoint: str = Field(..., description="The URL or route of the API endpoint.")
    method: str = Field(..., description="The HTTP method used by the API endpoint (e.g., GET, POST, PUT, DELETE).")
    description: Optional[str] = Field(None, description="Details about the API endpoint, including its purpose and usage.")
    input_parameters: Optional[dict] = Field(None, description="Expected input parameters for the API endpoint.")
    output_structure: Optional[dict] = Field(None, description="Structure of the API response.")


class APIOutput(BaseModel):
    apis: List[API] = Field(..., description="List of API endpoints, their methods, and detailed descriptions.")


class APIDBTable(BaseModel):
    endpoint: str = Field(..., description="The URL or route of the API endpoint.")
    method: str = Field(..., description="The HTTP method used by the API endpoint.")
    description: Optional[str] = Field(None, description="Details about the API, its use case, and expected behavior.")
    database_tables: List[str] = Field(..., description="List of database tables used by the API endpoint.")
    operations: List[str] = Field(..., description="List of database operations performed (e.g., SELECT, INSERT, UPDATE, DELETE).")
    sql_queries: List[str] = Field(..., description="List of SQL queries executed by the API")


class APIDBTableOutput(BaseModel):
    mappings: List[APIDBTable] = Field(..., description="Mappings of API endpoints to database tables and operations.")