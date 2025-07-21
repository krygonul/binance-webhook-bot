from binance.client import Client
import os

api_key = os.getenv("API_KEY", "")
api_secret = os.getenv("API_SECRET", "")

try:
    client = Client(api_key, api_secret, testnet=True)
    print("✅ Bağlantı başarılı:", client.ping())
except Exception as e:
    print("❌ Hata:", e)
