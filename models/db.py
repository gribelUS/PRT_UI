# Code written by Tiago Breunig

from dotenv import load_dotenv
import mysql.connector
import json
import os

# Load environment variables from .env
load_dotenv()

# Load MySQL configuration from JSON file
def load_config():
    path = os.path.join("config", "config.json")
    with open(path) as f:
        return json.load()[mysql]
    
# Create a connection to the MySQL database
def get_connection():
    config = load_config()
    return mysql.connector.connect(
        host = config["host"],
        user = config["user"],
        password = config["password"],
        database = config["database"]
    )

# Log a cart event
def log_event(cart_id, position, event_type):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO cart_logs (cart_id, position, event_type)
            VALUES (%s, %s, %s)
            """
        cursor.execute(sql, (cart_id, position, event_type))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"MySQL log error: {e}")