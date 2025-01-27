import streamlit as st
import os
import json
from dotenv import load_dotenv
from src.codebase_repo_agent.utils import generate_hashid

# Load environment variables
cwd = os.getcwd()
load_dotenv()

# Streamlit app layout
st.title("GitHub Codebase Analyzer")

# Initialize session state for repository path and page selection
if "repo_path" not in st.session_state:
    st.session_state.repo_path = None
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Landing Page"

# Input for repository path
repo_path = st.text_input("Enter the GitHub repository path or local directory path:")

# Ensure Analyze Codebase button is always visible
analyze_button = st.button("Analyze Codebase")

if analyze_button:  # Button pressed
    if repo_path:  # Check if a valid path is entered
        # Generate hash ID for the given path
        hash_id = generate_hashid(repo_path)
        st.session_state.repo_path = hash_id

        # Define directory paths
        repo_dir = os.path.join(cwd, "repo", hash_id)
        responses_dir = os.path.join(cwd, "responses", hash_id)

        # Function to process the codebase
        def process_codebase(path):
            if "https" in path:
                # Clone the GitHub repository
                from src.codebase_repo_agent.utils import clone_repo
                target_dir = clone_repo(path)
                from src.codebase_repo_agent.crew import GitHubCrew
                GitHubCrew().crew().kickoff(inputs={"codebase_path": target_dir})
            else:
                # Process the local directory
                from src.codebase_repo_agent.utils import copy_directory
                target_dir = copy_directory(path)
                from src.codebase_repo_agent.crew import GitHubCrew
                GitHubCrew().crew().kickoff(inputs={"codebase_path": target_dir})

        # Check if directories exist for the given hash ID
        with st.spinner("Processing..."):
            if not os.path.exists(repo_dir) or not os.path.exists(responses_dir):
                os.makedirs(repo_dir, exist_ok=True)
                os.makedirs(responses_dir, exist_ok=True)
                process_codebase(repo_path)
                st.success("Processing complete. Files are ready!")

        # Switch to Markdown Report view after processing
        st.session_state.page_selection = "Markdown Report"
    else:
        st.error("Please enter a valid repository path to analyze.")
else:
    st.info("Enter a repository path and click the **Analyze Codebase** button to begin.")

# Sidebar navigation (display only after a valid repository is processed)
if st.session_state.repo_path:
    st.sidebar.subheader("Navigation")
    st.session_state.page_selection = st.sidebar.radio(
        "Select Page:", ["Markdown Report", "JSON Files"], index=["Markdown Report", "JSON Files"].index(st.session_state.page_selection)
    )

# Display content based on page selection
if st.session_state.page_selection == "Markdown Report":
    st.title("Generated Markdown Report:")
    json_output_dir = os.path.join(cwd, "responses", st.session_state.repo_path)
    try:
        markdown_files = [
            file for file in os.listdir(json_output_dir) if file.endswith(".md")
        ]
        if markdown_files:
            markdown_file_path = os.path.join(json_output_dir, markdown_files[0])
            with open(markdown_file_path, "r") as f:
                st.markdown(f.read())

            # Provide download link for Markdown
            with open(markdown_file_path, "r") as f:
                st.download_button(
                    label="Download Markdown Report",
                    data=f,
                    file_name=markdown_files[0],
                    mime="text/markdown",
                )
        else:
            st.warning("No Markdown file found.")
    except Exception as e:
        st.warning("No Markdown file found.")
elif st.session_state.page_selection == "JSON Files":
    st.title("View JSON Files")
    json_output_dir = os.path.join(cwd, "responses", st.session_state.repo_path)
    try:
        json_files = [
            file for file in os.listdir(json_output_dir) if file.endswith(".json")
        ]
        if json_files:
            json_file_selected = st.selectbox("Choose a JSON file to view:", json_files)
            if json_file_selected:
                json_file_path = os.path.join(json_output_dir, json_file_selected)
                with open(json_file_path, "r") as f:
                    st.json(json.load(f))

                # Provide download link for JSON
                with open(json_file_path, "r") as f:
                    st.download_button(
                        label="Download JSON File",
                        data=f,
                        file_name=json_file_selected,
                        mime="application/json",
                    )
        else:
            st.warning("No JSON files found.")
    except Exception as e:
        st.warning("No JSON files found.")