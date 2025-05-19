# db.py
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Allowed positions (enum values)
ALLOWED_POSITIONS = {
    'Station_1', 'Station_2', 'Station_3', 'Station_4',
    'Segment_A', 'Segment_B', 'Segment_C', 'Segment_D',
    'Segment_E', 'Segment_F'
}

# Load MySQL config
def load_config():
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DB", "prt_system")
    }

# Connect to MySQL
def get_connection():
    config = load_config()
    print("🔍 db.py: Running get_connection()")
    print(f"Connecting to MySQL with config: {config}")
    try:
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ MySQL connection established.")
        print("🟢 get_connection(): returning connection object")
        return conn
    except Exception as err:
        import traceback
        print(f"❌ Database connection failed: {err}")
        traceback.print_exc()
        raise

# Log a cart event with validation
def log_event(cart_id, position, event_type):
    if position not in ALLOWED_POSITIONS:
        raise ValueError(f"Invalid position: {position}")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cart_logs (cart_id, position, event_type) VALUES (%s, %s, %s)",
            (cart_id, position, event_type)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"📦 Logged event: {cart_id}, {position}, {event_type}")
    except Exception as e:
        print(f"❌ Error logging event: {e}")

# Get latest info
def get_cart_info(cart_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM cart_logs WHERE cart_id = %s ORDER BY time_stamp DESC LIMIT 1",
            (cart_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"📋 Cart info for {cart_id}: {result}")
        return result
    except Exception as e:
        print(f"❌ Error fetching cart info: {e}")
        return None
