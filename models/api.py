import requests
from models.db import get_connection
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/prt/dest', methods=['POST'])
def send_cart_to_station(cart_id, station_id):
    """
    Send a request to the API to move a cart to a specific station.
    """
    api_url = "http://localhost:2650/prt/dest"
    payload = {
        "barcode": cart_id,
        "destination": station_id
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO cart_logs (cart_id, position, event_type, time_stamp)
                VALUES (%s, %s, %s, %s)"""
            data = (cart_id, station_id, 'sent', datetime.datetime.now())
            cursor.execute(query, data)
            conn.commit()

            cursor.close()
            conn.close()
        else:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO cart_logs (cart_id, position, event_type, time_stamp)
                VALUES (%s, %s, %s, %s)"""
            data = (cart_id, station_id, 'error', datetime.datetime.now())
            cursor.execute(query, data)
            conn.commit()

            cursor.close()
            conn.close()
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")
