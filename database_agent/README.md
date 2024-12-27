# Database SQL Agent

## Overview

The **Database SQL Agent** is a modular and intelligent system designed to streamline the process of extracting, analyzing, and reporting data from databases. Built using **Crew AI** and **LangChain**, it employs a team of specialized agents, each with distinct expertise, to ensure efficient data processing and insightful reporting.

---

## Key Components

### Agents

#### **SQL Developer (`sql_dev`)**
- **Role**: Senior Database Developer
- **Goal**: Design and execute SQL queries based on a given `{query}`.
- **Backstory**:  
  A seasoned database engineer, skilled in crafting efficient and complex SQL queries. Utilizes tools like `list_tables` for discovering tables, `tables_schema` for understanding metadata, `execute_sql` for validating queries, and `check_sql` for executing them on the database.

#### **Data Analyst (`data_analyst`)**
- **Role**: Senior Data Analyst
- **Goal**: Analyze the data provided by the database developer using Python (if required) and generate actionable insights for `{query}`.
- **Backstory**:  
  Experienced in analyzing datasets with precision, producing concise and actionable insights. Delivers results with a strong focus on clarity and attention to detail.

#### **Report Writer (`report_writer`)**
- **Role**: Senior Report Editor
- **Goal**: Write an executive summary report based on the work of the data analyst.
- **Backstory**:  
  Renowned for clear and effective communication, specializes in summarizing detailed analyses into concise bullet points for quick comprehension.

---

### Tasks

#### **1. Extract Data (`extract_data`)**
- **Description**: Extract data required for the query `{query}`.
- **Expected Output**: Database result for the query.
- **Agent**: SQL Developer (`sql_dev`).

#### **2. Analyze Data (`analyze_data`)**
- **Description**: Analyze the data extracted from the database and provide detailed insights for `{query}`.
- **Expected Output**: Detailed analysis text.
- **Agent**: Data Analyst (`data_analyst`).

#### **3. Write Report (`write_report`)**
- **Description**: Create an executive summary of the analysis. The report must be concise (less than 100 words).
- **Expected Output**: Markdown report.
- **Agent**: Report Writer (`report_writer`).

---

## How It Works

1. **Task Initiation**: A query `{query}` is provided as input to the system.  
2. **Data Extraction**:  
   - The `sql_dev` agent designs and executes the necessary SQL queries.  
   - The extracted data is validated and formatted as per the requirements.
3. **Data Analysis**:  
   - The `data_analyst` agent analyzes the extracted data, applying Python-based techniques if required.  
   - Insights and patterns are generated based on the query context.
4. **Report Generation**:  
   - The `report_writer` agent compiles the analysis into a concise executive summary.  
   - The output is delivered in a clear, markdown-based report.

---

## Features

- **Specialized Agent Collaboration**: Leverages distinct agent roles for SQL querying, data analysis, and reporting.  
- **Dynamic Task Handling**: Ensures tasks are routed to the appropriate expert agent.  
- **Integrated Workflows**: Seamlessly connects data extraction, analysis, and reporting processes.  
- **Efficient Outputs**: Generates detailed and actionable results tailored to the input query.  

---

## Requirements

- **Python 3.11**
- **LangChain**
- **Crew AI**

---
