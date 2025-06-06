import os
from flask import Flask, request, jsonify
from models.db import log_event

app = Flask(__name__)

# Map locations from PLC payloads to valid cart_logs position values
POSITION_MAP = {
    "Sorter 1": "Segment_A",
    "Station 1": "Station_1",
    "Station 2": "Station_2",
    "Station 3": "Station_3",
    "Station 4": "Station_4",
}

@app.route('/plc/update', methods=['POST'])
def plc_update():
    data = request.get_json(force=True)
    cart_id = data.get('barcode')
    location = data.get('location')
    status = data.get('status')
    if not cart_id or not location:
        return jsonify({'error': 'barcode and location required'}), 400

    position = POSITION_MAP.get(location, location)
    try:
        log_event(str(cart_id), position, status or '')
        return jsonify({'message': 'logged'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/log_event', methods=['GET'])
def create_log():
    cart_id = request.args.get('cart_id')
    position = request.args.get('position')
    event_type = request.args.get('event_type', 'manual')
    if not cart_id or not position:
        return jsonify({'error': 'cart_id and position required'}), 400
    try:
        log_event(cart_id, position, event_type)
        return jsonify({'message': 'logged'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('LOG_SERVER_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
