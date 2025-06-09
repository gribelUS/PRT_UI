import requests

url = "http://localhost:5000/plc/update"
payload = {
    "barcode": "CART123",
    "location": "Sorter 1",
    "status": "arrived"
}
resp = requests.post(url, json=payload)
print(resp.status_code, resp.text)
