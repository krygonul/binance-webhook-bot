import requests

r = requests.post("http://127.0.0.1:5000/webhook", json={"test": "merhaba"})
print("Yanıt:", r.status_code)
print("Cevap:", r.text)
