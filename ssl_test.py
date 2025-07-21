import requests

try:
    response = requests.get("https://api.binance.com/api/v3/ping", verify=False)
    print("✅ Çalıştı:", response.text)
except Exception as e:
    print("❌ Hata:", e)
