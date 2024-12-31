import streamlit as st
import os
from phi.agent import Agent
from phi.model.google import Gemini
from prompts import SYSTEM_PROMPT, INSTRUCTIONS
from phi.tools.tavily import TavilyTools

if "response_content" not in st.session_state:
    st.session_state.response_content = ''


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
            "Analyze the given image, donot include any starting response from your end",
            images=[image_path],
        )
        st.session_state.response_content = response.content
        # Use Streamlit container for custom layout and styling
        with st.container():
            # Header for the analysis result
            st.subheader("Analysis Result")

            # Displaying the response in a formatted, indented way using markdown
            with st.expander("Click to expand detailed analysis"):
                st.markdown(f"""
                <div style="background-color: white; color: black; padding: 20px; border-radius: 10px;">
                    <p>{st.session_state.response_content}</p>
                </div>
            """, unsafe_allow_html=True)

            # If the response contains JSON or structured data, we can show it as code
            if isinstance(st.session_state.response_content, dict) or isinstance(st.session_state.response_content, list):
                st.code(response.content, language='json')

            # Optionally, you can add a footer or note
            st.markdown("---")
            st.markdown("*Analysis powered by AI. Feel free to provide more context.*")
            download_report()


@st.fragment
def download_report():
    # Prepare the Markdown content for download
    markdown_content = st.session_state.response_content

    # Add download button for Markdown file
    st.download_button(
        label="Download Report as Markdown",
        data=markdown_content,
        file_name="Report.md",
        mime="text/markdown",
        icon=':material/download_2:',
        type='primary'
    )
