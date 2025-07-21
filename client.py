from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
TESTNET = os.getenv("TESTNET", "true").lower() == "true"

base_url = "https://api.binance.com"

client = Client(API_KEY, API_SECRET)
client.API_URL = "https://testnet.binance.vision"

