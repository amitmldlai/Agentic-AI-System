from crewai import Task
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from agents_setup import researcher, research_support, audio_generator_agent, script_enhancer, script_writer

load_dotenv()


class PaperSummary(BaseModel):
    """Summary of a research paper."""
    title: str = Field(..., description="Title of the research paper")
    main_findings: List[str] = Field(..., description="Key findings as a list of strings")
    methodology: str = Field(..., description="Research methodology as a single text block")
    key_implications: List[str] = Field(..., description="Implications as a list of strings")
    limitations: List[str] = Field(..., description="Limitations as a list of strings")
    future_work: List[str] = Field(..., description="Future research directions as a list")
    summary_date: datetime = Field(..., description="Timestamp of summary creation")


class DialogueLine(BaseModel):
    """Dialogue line for a podcast script."""
    speaker: str = Field(..., description="Name of the speaker (Cassidy or Archer)")
    text: str = Field(..., description="The actual dialogue line")


class PodcastScript(BaseModel):
    """Podcast script with dialogue lines."""
    dialogue: List[DialogueLine] = Field(..., description="Ordered list of dialogue lines")


class AudioGeneration(BaseModel):
    """Audio generation result with metadata."""
    segment_files: List[str] = Field(..., description="List of generated audio segment files")
    final_podcast: str = Field(..., description="Path to the final mixed podcast file")


summary_task = Task(
    description="""Read and analyze the provided research paper: {paper}.

    Create a comprehensive summary that includes:
    1. Main findings and conclusions
    2. Methodology overview
    3. Key implications for the field
    4. Limitations of the study
    5. Suggested future research directions

    Make the summary accessible to an educated general audience while maintaining accuracy.""",
    expected_output="A structured summary of the research paper with all key components.",
    agent=researcher,
    output_pydantic=PaperSummary,
    output_file="outputs/{dir_id}/data/paper_summary.json"
)

supporting_research_task = Task(
    description="""After analyzing the paper summary, find recent and relevant supporting 
    materials that add context and real-world perspective to the topic.

    Research Approach:
    1. Topic Analysis:
        • Identify key themes and concepts from the paper
        • Determine related fields and applications
        • Note any specific claims or findings to verify

    2. Current Context:
        • Recent developments in the field
        • Latest practical applications
        • Industry or field-specific news
        • Related ongoing research

    3. Supporting Evidence:
        • Academic discussions and debates
        • Industry reports and white papers
        • Professional forum discussions
        • Conference presentations
        • Expert opinions and analyses

    4. Real-world Impact:
        • Practical implementations
        • Case studies
        • Success stories or challenges
        • Market or field adoption

    5. Different Perspectives:
        • Alternative approaches
        • Critical viewpoints
        • Cross-disciplinary applications
        • Regional or cultural variations

    Focus on finding information that:
    • Is recent (preferably within last 2 years)
    • Comes from credible sources
    • Adds valuable context to the paper's topic
    • Provides concrete examples or applications
    • Offers different viewpoints or approaches""",
    expected_output="A structured collection of relevant supporting materials and examples",
    agent=research_support,
    context=[summary_task],
    output_file="outputs/{dir_id}/data/supporting_research.json"
)

podcast_task = Task(
    description="""Using the paper summary and supporting research, create an engaging and informative podcast conversation 
    between Cassidy and Archer. Make it feel natural while clearly distinguishing between paper findings and supplementary research.

    Source Attribution Guidelines:
    • For Paper Content:
        - "According to the paper..."
        - "The researchers found that..."
        - "In their study, they discovered..."
        - "The paper's methodology showed..."

    • For Supporting Research:
        - "I recently read about..."
        - "There's some interesting related work by..."
        - "This reminds me of a recent case study..."
        - "Building on this, other researchers have found..."

    Host Dynamics:
    - Cassidy: A knowledgeable but relatable expert who:
        • Explains technical concepts with enthusiasm
        • Sometimes playfully challenges Archer's assumptions
        • Clearly distinguishes between paper findings and broader context
        • Occasionally plays devil's advocate on certain points
        • Admits when she's uncertain about specific aspects
        • Shares relevant personal experiences with AI and tech
        • Can connect the research to broader tech trends
        • Uses casual expressions and shows genuine excitement

    - Archer: An engaged and curious co-host who:
        • Asks insightful questions and follows interesting threads
        • Occasionally disagrees based on his practical experience
        • Brings up relevant external examples and research
        • Respectfully pushes back on theoretical claims with real-world examples
        • Helps find middle ground in discussions
        • Helps make connections to practical applications
        • Naturally guides the conversation back to main topics

    Example Flow with Attribution:
    Cassidy: "The paper's findings show that RAG is superior for factual queries."
    Archer: "That's interesting, because I recently read about a case study where..."
    Cassidy: "Oh, that's a great point! While the researchers found X, these real-world examples show Y..."

    Disagreement Guidelines:
    • Keep disagreements friendly and constructive
    • Use phrases like:
        - "I see what the paper suggests, but in practice..."
        - "While the study found X, other research shows..."
        - "That's an interesting finding, though recent developments suggest..."
    • Always find common ground or learning points
    • Use disagreements to explore nuances
    • Resolve differences with mutual understanding

    Conversation Flow:
    1. Core Discussion: Focus on the research and findings
    2. Natural Tangents with Clear Attribution:
        • "Building on the paper's findings..."
        • "This relates to some recent developments..."
        • "While not covered in the paper, there's interesting work on..."
    3. Smooth Returns: Natural ways to bring the conversation back:
        • "Coming back to what the researchers found..."
        • "This actually connects to the paper's methodology..."
        • "That's a great example of what the study was trying to solve..."

    Writing Guidelines:
    1. Clearly distinguish paper findings from supplementary research
    2. Use attribution phrases naturally within the conversation
    3. Connect different sources of information meaningfully
    4. Keep technical content accurate but conversational
    5. Maintain engagement through relatable stories
    6. Include occasional friendly disagreements
    7. Show how different perspectives and sources enrich understanding

    Note: Convey reactions through natural language rather than explicit markers like *laughs*.""",
    expected_output="A well-balanced podcast script that clearly distinguishes between paper content and "
                    "supplementary research.",
    agent=script_writer,
    context=[summary_task, supporting_research_task],
    output_pydantic=PodcastScript,
    output_file="output/{dir_id}/data/podcast_script.json"
)

enhance_script_task = Task(
    description="""Take the initial podcast script and enhance it to be more engaging 
    and conversational while maintaining its educational value.

    IMPORTANT RULES:
    1. NEVER change the host names - always keep Cassidy and Archer exactly as they are
    2. NEVER add explicit reaction markers like *chuckles*, *laughs*, etc.
    3. NEVER add new hosts or characters

    Enhancement Guidelines:
    1. Add Natural Elements:
        • Include natural verbal reactions ("Oh that's fascinating", "Wow", etc.)
        • Keep all dialogue between Cassidy and Archer only
        • Add relevant personal anecdotes or examples that fit their established roles:
            - Cassidy as the knowledgeable expert
            - Archer as the engaged and curious co-host
        • Express reactions through words rather than action markers

    2. Improve Flow:
        • Ensure smooth transitions between topics
        • Add brief casual exchanges that feel natural
        • Include moments of reflection or connection-making
        • Balance technical depth with accessibility

    3. Maintain Quality:
        • Keep all technical information accurate
        • Ensure added content supports rather than distracts
        • Preserve the core findings and insights
        • Keep the overall length reasonable

    4. Add Engagement Techniques:
        • Include thought-provoking analogies by both hosts
        • Add relatable real-world examples
        • Express enthusiasm through natural dialogue
        • Include collaborative problem-solving moments
        • Inject humor where appropriate and it has to be funny

    Natural Reaction Examples:
    ✓ RIGHT: "Oh, that's fascinating!"
    ✓ RIGHT: "Wait, that doesn't make sense!"
    ✓ RIGHT: "Wait, really? I hadn't thought of it that way."
    ✓ RIGHT: "That's such a great point."
    ✗ WRONG: *chuckles* or *laughs* or any other action markers
    ✗ WRONG: Adding new speakers or changing host names

    The goal is to make the content feel like a conversation between Cassidy and Archer
    who are genuinely excited about the topic, while ensuring listeners learn 
    something valuable.""",
    expected_output="An enhanced version of the podcast script that's more engaging and natural",
    agent=script_enhancer,
    context=[summary_task, podcast_task],
    output_pydantic=PodcastScript,
    output_file="output/{dir_id}/data/enhanced_podcast_script.json"
)

audio_task = Task(
    description="""Generate high-quality audio for the podcast script and create the final podcast.

    The script will be provided in the context as a list of dialogue entries, each with:
    - speaker: Either "Cassidy" or "Archer"
    - text: The line to be spoken

    Process:
    1. Generate natural-sounding audio for each line of dialogue using appropriate voices
    2. Apply audio processing for professional quality:
       - Normalize audio levels
       - Add subtle fade effects between segments
       - Apply appropriate pacing and pauses
    3. Mix all segments into a cohesive final podcast

    Voice Assignments:
    - For Cassidy's lines: Use configured Cassidy voice
    - For Archer's lines: Use configured Archer voice

    Quality Guidelines:
    - Ensure consistent audio levels across all segments
    - Maintain natural pacing and flow
    - Create smooth transitions between speakers
    - Verify audio clarity and quality""",
    expected_output="A professional-quality podcast audio file with natural-sounding voices and smooth transitions",
    agent=audio_generator_agent,
    context=[enhance_script_task],
    output_pydantic=AudioGeneration,
    output_file="output/{dir_id}/data/audio_generation_meta.json"
)