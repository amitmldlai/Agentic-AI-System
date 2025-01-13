from crewai import Crew, Process
from dotenv import load_dotenv
from tasks_setup import *
load_dotenv()

crew = Crew(
    agents=[research_agent, professional_writer_agent],
    tasks=[answer_customer_question_task, write_email_task],
    process=Process.sequential,
)


while True:
    customer_question = input("Which section of the report would you like to generate a work order for?\n")
    contractor_name = input("Name of the contractor to send the email\n")
    contractor_email = input("Email id of the contractor\n")

    result = crew.kickoff(inputs={"customer_question": customer_question, "contractor_name": contractor_name,
                                  "contractor_email": contractor_email})
    print(result)