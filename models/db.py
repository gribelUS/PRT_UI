# Code written by Tiago Breunig

from dotenv import load_dotenv
import mysql.connector
import json
import os

# Load environment variables from .env
load_dotenv()

# Load MySQL configuration from JSON file
def load_config():
    return {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DB")
    }
    
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

# Get cart information
def get_cart_info(cart_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM cart_logs
            WHERE cart_id = %s
            ORDER BY time_stamp DESC
            LIMIT 1
        """, (cart_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"DB Error: {e}")
        return None
