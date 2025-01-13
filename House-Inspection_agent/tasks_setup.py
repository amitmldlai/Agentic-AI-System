from crewai import Task
from tools_setup import pdf_search_tool
from agents_setup import research_agent, professional_writer_agent
answer_customer_question_task = Task(
    description=(
        """
        Answer the customer's questions based on the home inspection PDF.
        The research agent will search through the PDF to find the relevant answers.
        Your final answer MUST be clear and accurate, based on the content of the home
        inspection PDF.

        Here is the customer's question:
        {customer_question}
        """
    ),
    expected_output="""
        Provide clear and accurate answers to the customer's questions based on 
        the content of the home inspection PDF.
        """,
    tools=[pdf_search_tool],
    agent=research_agent,
)

write_email_task = Task(
    description=(
        """
        - Write a professional email and send it to a contractor based 
            on the research agent's findings.
        - The email should clearly state the issues found in the specified section 
            of the report and request a quote or action plan for fixing these issues.
        - Split the email content across multiple lines, with the request for quote or 
           action plan for fixing these issues in last line. Align the email content like professional.
        - Ensure the email is signed with the following details:
            Hello {contractor_name}

            Best regards,
            Amit
        - Contractor email address: {contractor_email}     
        """
    ),
    expected_output="""
        Write a clear and concise email and send it to a contractor to address the 
        issues found in the home inspection report.
        """,
    tools=[],
    agent=professional_writer_agent,
    output_file='Final.eml'
)
