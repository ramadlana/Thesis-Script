import requests

headers = {
    'accept': 'application/json',
}

response = requests.get('http://127.0.0.1:8000/info-tunnel', headers=headers)
response = response.json()
print(response["fec_status"])