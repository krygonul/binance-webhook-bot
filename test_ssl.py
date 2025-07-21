import requests

try:
    res = requests.get("https://api.binance.com/api/v3/ping")
    print("✅ Başarılı:", res.text)
except requests.exceptions.SSLError as e:
    print("❌ SSL Hatası:", e)
except Exception as e:
    print("❌ Genel Hata:", e)
