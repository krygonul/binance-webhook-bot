import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://testnet.binancefuture.com"

def get_account_info():
    endpoint = "/fapi/v2/account"
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}{endpoint}?{query_string}&signature={signature}"

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    response = requests.get(url, headers=headers)
    print(response.status_code, response.text)

if __name__ == "__main__":
    get_account_info()
