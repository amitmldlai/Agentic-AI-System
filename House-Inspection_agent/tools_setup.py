from crewai_tools import PDFSearchTool
import smtplib
from email.message import EmailMessage
from crewai.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
pdf_search_tool = PDFSearchTool(pdf="./data/home_inspection.pdf",
                                config=dict(
                                        llm=dict(provider="google", config=dict(model="gemini/gemini-1.5-flash")),
                                        embedder=dict(provider="google", config=dict(model="models/text-embedding-004"))
                                        ))


@tool("EmailSender")
def send_email_gmail(tool_input):
    """
    Sends an email using Gmail api,
    contractor_email (str): The recipient's email address.
    subject (str): The subject of the email.
    body (str): The body of the email.

    tool_input should  be json
    Example:
        {
        "contractor_email" : Contractor email address,
         "subject" : Subject for the mail,
         "body" : Content of the mail, which the agent prepared
        }
    """
    tool_input = eval(tool_input)
    contractor_email, subject, body = (tool_input.get("contractor_email"), tool_input.get("subject"),
                                       tool_input.get("body"))
    try:
        # Create the email message
        sender_email = os.getenv("sender_email")
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = contractor_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, os.getenv("sender_password"))  # Login to your Gmail account
            smtp.send_message(msg)  # Send the email

        return f"Email successfully sent to {contractor_email}"
    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"


