from datetime import datetime
import os
from crewai import LLM
import uuid
from dotenv import load_dotenv

load_dotenv()


def setup_directories():
    """Set up organized directory structure"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_id = uuid.uuid4()
    dirs = {
        'BASE': f'outputs/{dir_id}',
        'SEGMENTS': f'outputs/{dir_id}/segments',  # Individual voice segments
        'FINAL': f'outputs/{dir_id}/podcast',  # Final podcast file
        'DATA': f'outputs/{dir_id}/data'  # Metadata/JSON files
    }

    for directory in dirs.values():
        os.makedirs(directory, exist_ok=True)

    return dirs, dir_id


def setup_llm():
    summary_llm = LLM(
        model="openai/o1-preview",
        temperature=0.0,
    )

    script_llm = LLM(
        model="gemini/gemini-1.5-pro",
        temperature=0.3,
    )

    script_enhancer_llm = LLM(
        model="anthropic/claude-3-5-sonnet-20241022",
        temperature=0.7,
    )

    audio_llm = LLM(
        model="cerebras/llama3.3-70b",
        temperature=0.0,
    )

    all_llm = {
        "summary_llm": summary_llm,
        "script_llm": script_llm,
        "script_enhancer_llm": script_enhancer_llm,
        "audio_llm": audio_llm,
    }

    return all_llm


# llm = setup_llm()
# resp = llm["summary_llm"].call(messages=[{"role": "user", "content": "Hi"}])
# print(resp)