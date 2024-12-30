import streamlit as st
import os
from phi.agent import Agent
from phi.model.google import Gemini
from prompts import SYSTEM_PROMPT, INSTRUCTIONS
from phi.tools.tavily import TavilyTools


@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        markdown=True,
    )


def analyze_image(image_path):
    agent = get_agent()
    with st.spinner('Analyzing image...'):
        response = agent.run(
            "Analyze the given image",
            images=[image_path],
        )
        st.markdown(response.content)