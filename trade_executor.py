from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TESTNET = os.getenv("TESTNET", "true").lower() == "true"

client = Client(API_KEY, API_SECRET)

# 🔁 Testnet ise URL'yi manuel override et
if TESTNET:
    client.API_URL = "https://testnet.binance.vision"

def execute_trade(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        print(f"✅ Order executed: {order}")
    except Exception as e:
        print(f"❌ Trade failed: {e}")
