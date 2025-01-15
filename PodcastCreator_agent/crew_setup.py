from crewai import Crew, Process
import os
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from agents_setup import researcher, research_support, script_writer, script_enhancer, audio_generator_agent
from tasks_setup import summary_task, supporting_research_task, podcast_task, enhance_script_task, audio_task
from utils import setup_directories

dirs, dir_id = setup_directories()
research_paper = PDFKnowledgeSource(file_path="RAG.pdf")

crew = Crew(
    agents=[researcher, research_support, script_writer, script_enhancer, audio_generator_agent],
    tasks=[summary_task, supporting_research_task, podcast_task, enhance_script_task, audio_task],
    process=Process.sequential,
    knowledge_sources=[research_paper],
    verbose=True
)

# Update task output files
summary_task.output_file = os.path.join(dirs['DATA'], "paper_summary.json")
supporting_research_task.output_file = os.path.join(dirs['DATA'], "supporting_research.json")
podcast_task.output_file = os.path.join(dirs['DATA'], "podcast_script.json")
enhance_script_task.output_file = os.path.join(dirs['DATA'], "enhanced_podcast_script.json")
audio_task.output_file = os.path.join(dirs['DATA'], "audio_generation_meta.json")

# Run the podcast generation process
results = crew.kickoff(inputs={"paper": "RAG.pdf", "dir_id": dir_id})