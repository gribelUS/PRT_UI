import requests
import time
import random

def simulate_cart_report():
    barcodes = [1001, 1002, 1003, 1004]
    locations = ["Segment_A", "Station_2", "Segment_B"]
    statuses = ["good", "diverted"]

    for _ in range(10):  # Send 10 fake updates
        barcode = random.choice(barcodes)
        location = random.choice(locations)
        status = random.choice(statuses)

        payload = {
            "cart_id": barcode,
            "position": location,
            "event_type": status
        }

        try:
            response = requests.post("http://localhost:5000/plc/update", json=payload)
            if response.ok:
                print(f"✅ Sent: {payload}")
            else:
                print(f"⚠️ Failed ({response.status_code}): {payload}")
        except Exception as e:
            print(f"❌ Error sending: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    simulate_cart_report()
