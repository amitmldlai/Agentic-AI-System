import sqlite3
import pandas as pd


def create_db():
    try:
        df = pd.read_csv("../data/ds-salaries.csv")
        connection = sqlite3.connect("../data/salaries.db")
        df.to_sql(name="salaries", con=connection)
        return "Database created."
    except Exception as e:
        return f"Error occurred: {e}"


print(create_db())