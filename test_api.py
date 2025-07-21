import requests

try:
    response = requests.get("https://api.binance.com/api/v3/ping")
    print("✅ Başarılı cevap:", response.json())
except Exception as e:
    print("❌ Hata:", e)
