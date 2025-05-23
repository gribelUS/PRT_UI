from flask import Flask, request, jsonify
from models.db import get_connection
import datetime

app = Flask(__name__)
@app.route('/plc/update', methods=['POST'])
def plc_update():
    data = request.json
    cart_id = data.get("cart_id")
    position = data.get("position")
    event_type = data.get("event_type")

    if not cart_id or not position or not event_type:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO cart_logs (cart_id, position, event_type, time_stamp)
        VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.datetime.now()
        cursor.execute(query, (cart_id, position, event_type, timestamp))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to insert into DB: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)