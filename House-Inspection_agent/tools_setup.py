from crewai_tools import PDFSearchTool
from email.message import EmailMessage
from pydantic import BaseModel, Field
from typing import Type
import smtplib
from crewai.tools import BaseTool
from dotenv import load_dotenv
import os

load_dotenv()

pdf_search_tool = PDFSearchTool(pdf="./data/home_inspection.pdf",
                                config=dict(
                                        llm=dict(provider="google", config=dict(model="gemini/gemini-1.5-flash")),
                                        embedder=dict(provider="google", config=dict(model="models/text-embedding-004"))
                                        ))


class EmailSenderInput(BaseModel):
    """Input schema for sending an email using Gmail."""
    contractor_email: str = Field(..., description="The recipient's email address.")
    subject: str = Field(..., description="The subject of the email.")
    body: str = Field(..., description="The body content of the email.")


class EmailSenderOutput(BaseModel):
    """Output schema for the email sender tool."""
    success: bool = Field(..., description="Whether the email was successfully sent.")
    error_message: str = Field(
        None, description="Error message if the email failed to send."
    )


class EmailSenderTool(BaseTool):
    name: str = "EmailSender"
    description: str = "Sends an email using Gmail."
    args_schema: Type[BaseModel] = EmailSenderInput
    return_schema: Type[BaseModel] = EmailSenderOutput

    def _run(self, contractor_email: str, subject: str, body: str) -> EmailSenderOutput:
        try:
            # Retrieve sender credentials from environment variables
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")
            if not sender_email or not sender_password:
                raise ValueError("Sender email or password not set in environment variables.")

            # Create the email message
            msg = EmailMessage()
            msg['From'] = sender_email
            msg['To'] = contractor_email
            msg['Subject'] = subject
            msg.set_content(body)

            # Connect to Gmail's SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)  # Login to Gmail
                smtp.send_message(msg)  # Send the email

            return EmailSenderOutput(success=True, error_message=None)

        except Exception as e:
            return EmailSenderOutput(success=False, error_message=str(e))
