import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "latitude": 22.5726,
    "longitude": 88.3639
}

response = requests.post(url, json=data)
print(response.json())