# Food Review Crew

Welcome to the  Food Review Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

In this project, we focus on processing customer feedback about restaurants. The system starts by analyzing the review category (e.g., "good," "neutral," "bad") from the feedback provided. Based on the determined `review_category`, the appropriate crew is activated to handle further actions.

- If the review is positive (good), the system triggers a crew that sends a motivational response and encourages the customer to order again.
- If the review is neutral, the system suggests alternative restaurants to the customer and aims to improve the overall experience.
- If the review is negative, the system generates an apology message, offers a coupon code, and logs the feedback for further database management.

This workflow ensures that each type of review is processed with tailored responses and actions, ensuring efficient and meaningful customer engagement. Each crew is designed to handle specific review categories, enabling smooth collaboration and the appropriate handling of feedback across various scenarios.


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

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run or python main.py
```

## Understanding Your Crew

The food_review Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

