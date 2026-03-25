import mysql.connector as m
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def db_connect():
    try:
        db = m.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "warehouse"),
        )
        return db
    except m.Error as err:          
        print(f"Database connection error: {err}")
        return None
