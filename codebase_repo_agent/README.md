# CodebaseRepoAgent Crew

Welcome to the CodebaseRepoAgent Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## Activate the virtual environment:

On Windows:
```
.venv\Scripts\activate
```
On macOS/Linux:
```
source .venv/bin/activate
```

### Customizing

**Add your Keys and Model name into the `.env` file**
```
MODEL=[If using OPENAI model]
OPENAI_API_KEY=[Required,by default uses OPENAI model]
LLAMA_CLOUD_API_KEY=[Optional]
GEMINI_API_KEY=[If using Llama Parse]
GROQ_API_KEY=[Optional]
CEREBRAS_API_KEY=[Optional]
GOOGLE_API_KEY=[Optional]
```
## Running the Project

To kickstart your crew of AI agents and begin task execution, run the app:

```bash
$ streamlit run app.py
```

## Understanding Your Crew

The codebase_repo_agent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

