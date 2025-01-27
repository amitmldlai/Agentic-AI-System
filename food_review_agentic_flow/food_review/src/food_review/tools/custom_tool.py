from typing import Type
import sqlite3
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from food_review.src.food_review.models import DatabaseLoggerToolInput

DATABASE_URI = 'sqlite:///feedback.db'

# Example: Test connection
try:
    conn = sqlite3.connect("feedback.db")
    print("SQLite Connection Successful!")
except Exception as e:
    print("Error:", e)


class DatabaseLoggerTool(BaseTool):
    name: str = "Feedback Logger"
    description: str = (
        "This tool is responsible for logging customer feedback and restaurant information into the database. "
        "It helps in storing feedback for later analysis and tracking."
    )
    args_schema: Type[BaseModel] = DatabaseLoggerToolInput

    def _run(self, feedback_message: str, restaurant_name: str) -> str:
        """Inserts an entry in the feedback_table in SQLite, creating the table if it doesn't exist."""

        # Query to create the feedback_table if it doesn't already exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS feedback_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_message TEXT NOT NULL,
            restaurant_name TEXT NOT NULL
        )
        """

        # Query to insert feedback into the table
        insert_feedback_query = """
        INSERT INTO feedback_table (feedback_message, restaurant_name)
        VALUES (?, ?)
        """

        try:
            with sqlite3.connect("feedback.db") as conn:
                cursor = conn.cursor()

                # Create the table if it doesn't exist
                cursor.execute(create_table_query)

                # Insert the feedback into the table
                cursor.execute(insert_feedback_query, (feedback_message, restaurant_name))
                conn.commit()

            return "Feedback successfully inserted into the database."
        except Exception as e:
            return f"Error inserting feedback: {e}"
