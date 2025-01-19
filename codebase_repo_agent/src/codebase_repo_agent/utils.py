from git import Repo
import os
from crewai import LLM
import shutil
import stat
import glob
from hashids import Hashids
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
cwd = os.getcwd()


def clone_repo(repo_url):
    target_dir = os.path.join(cwd, "repo", st.session_state.repo_path)
    os.makedirs(target_dir, exist_ok=True)
    try:
        Repo.clone_from(repo_url, target_dir)
        print(f"Repository cloned successfully to {target_dir}")
        clean_directory(target_dir)
        return target_dir
    except Exception as e:
        print(f"Error occurred while cloning: {e}")


def copy_directory(src_dir):
    """Copy all directories and files from src_dir to dest_dir."""
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        return
    try:
        target_dir = os.path.join(cwd, "repo", st.session_state.repo_path)
        shutil.copytree(src_dir, target_dir, dirs_exist_ok=True)
        print(f"Successfully copied {src_dir} to {target_dir}")
        clean_directory(target_dir)
        return target_dir
    except Exception as e:
        print(f"Error occurred while copying: {e}")


def llm_mapping():
    llm = {
        'gemini': LLM(model='gemini/gemini-1.5-pro'),
        'openai': LLM(model='openai/gpt-4o'),
        'qroq': LLM(model='groq/llama-3.1-70b-versatile'),
        'cerebras': LLM(model='cerebras/llama3.1-70b')
    }
    return llm


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)  # Remove read-only attribute
    func(path)  # Call the original function to delete the file/folder


# Function to delete .git folder
def delete_folder(directory):
    directories = ['.git', '.idea', '__pycache__']
    for direct in directories:
        folder = os.path.join(directory, direct)  # Path to the .git folder
        try:
            # Check if the .git folder exists
            if os.path.exists(folder):
                # Recursively delete the .git folder and all of its contents
                shutil.rmtree(folder, onerror=remove_readonly)
                print(f"Successfully deleted: {folder}")
            else:
                print(f"{direct} folder not found in: {directory}")
        except PermissionError:
            print(f"Permission denied: {folder}")
        except Exception as e:
            print(f"Error while deleting {folder}: {e}")


# Function to remove files with extensions ending in 'ignore'
def remove_ignore_files(directory):
    # Glob pattern to match all files ending with 'ignore' (e.g., .gitignore, .ignore)
    pattern = directory + '/.*ignore'  # Matches files with extensions like .gitignore
    files_to_delete = glob.glob(pattern, recursive=True)

    # Loop through all matched files and delete them
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file
                print(f"Successfully deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except PermissionError:
            print(f"Permission denied: {file_path}")
        except Exception as e:
            print(f"Error while deleting {file_path}: {e}")


# Main function to clean the directory
def clean_directory(directory):
    # Remove .git folder
    delete_folder(directory)

    # Remove files ending with 'ignore'
    remove_ignore_files(directory)


def generate_hashid(input_string: str, salt="my_salt", max_length=32) -> str:
    """
    Generates an alphanumeric hash ID from a given string (path or URL).

    Parameters:
    - input_string: The URL or path to be hashed.
    - salt: A custom salt to be used for generating consistent hashes (optional).
    - max_length: The maximum length of the generated hash ID.

    Returns:
    - A consistent, alphanumeric hash ID (with max length).
    """
    # Create a Hashids object with a given salt and a specified minimum length for output
    hashids = Hashids(salt=salt, min_length=8)  # Set min_length to ensure a readable output

    # Generate a hash ID from the input string
    hashid = hashids.encode(*[ord(c) for c in input_string])  # Convert string to integers (ASCII values)

    # Limit the length of the hash ID to a maximum of max_length (e.g., 32 characters)
    return hashid[:max_length]