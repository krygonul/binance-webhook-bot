
import os
import time
import hmac
import hashlib
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

app = Flask(__name__)

def get_timestamp():
    return int(time.time() * 1000)

def sign(params):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def send_signed_request(http_method, url_path, payload={}):
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    payload["timestamp"] = get_timestamp()
    payload["signature"] = sign(payload)
    if http_method == "GET":
        return requests.get(BASE_URL + url_path, headers=headers, params=payload)
    elif http_method == "POST":
        return requests.post(BASE_URL + url_path, headers=headers, params=payload)
    elif http_method == "DELETE":
        return requests.delete(BASE_URL + url_path, headers=headers, params=payload)

def check_open_position(symbol):
    try:
        positions_resp = send_signed_request("GET", "/fapi/v2/positionRisk")
        positions = positions_resp.json()
        for p in positions:
            if p["symbol"] == symbol and float(p["positionAmt"]) != 0:
                return True
        return False
    except:
        return False

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    symbol = data.get("symbol")
    side = data.get("side", "BUY")
    params = data.get("params", {})

    if check_open_position(symbol):
        return jsonify({
            "status": "ignored",
            "message": f"{symbol} için açık pozisyon bulundu, sinyal reddedildi."
        })

    try:
        account_resp = send_signed_request("GET", "/fapi/v2/account")
        account_data = account_resp.json()
        if "totalWalletBalance" not in account_data:
            return jsonify({
                "status": "error",
                "message": "Hesap bilgisi alınamadı",
                "response": account_data
            })

        balance = float(account_data["totalWalletBalance"])
        entry_pip = float(params["entry_pip"])
        tp_pip = float(params["tp_pip"])
        sl_pip = float(params["sl_pip"])
        leverage = int(params["leverage"])
        pos_percent = float(params["position_size_percent"])

        # Fiyat ve miktar hesaplama
        mark_resp = requests.get(f"{BASE_URL}/fapi/v1/premiumIndex", params={"symbol": symbol})
        mark_price = float(mark_resp.json()["markPrice"])
        entry_price = mark_price + entry_pip if side == "BUY" else mark_price - entry_pip
        tp = entry_price + tp_pip if side == "BUY" else entry_price - tp_pip
        sl = entry_price - sl_pip if side == "BUY" else entry_price + sl_pip

        # Kaldıraç ayarla
        send_signed_request("POST", "/fapi/v1/leverage", {
            "symbol": symbol,
            "leverage": leverage
        })

        # Quantity hesapla
        notional = balance * leverage * (pos_percent / 100)
        quantity = round(notional / entry_price, 0)

        # Pozisyon aç (market order)
        open_order = send_signed_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        })

        # TP - Limit order
        tp_order = send_signed_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": "SELL" if side == "BUY" else "BUY",
            "type": "LIMIT",
            "quantity": quantity,
            "price": f"{tp:.6f}",
            "timeInForce": "GTC",
            "reduceOnly": "true"
        })

        # SL - Stop market
        sl_order = send_signed_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": "SELL" if side == "BUY" else "BUY",
            "type": "STOP_MARKET",
            "stopPrice": f"{sl:.6f}",
            "closePosition": "false",
            "quantity": quantity,
            "timeInForce": "GTC",
            "reduceOnly": "true"
        })

        return jsonify({
            "status": "executed",
            "entry_price": entry_price,
            "tp": tp,
            "sl": sl,
            "quantity": quantity,
            "side": side,
            "response": open_order.json(),
            "tp_order": tp_order.json(),
            "sl_order": sl_order.json()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route("/close", methods=["POST"])
def close_position():
    try:
        data = request.get_json()
        symbol = data.get("symbol")
        side = data.get("side")

        if not symbol or not side:
            return jsonify({"status": "error", "message": "symbol ve side zorunlu."})

        close_order = send_signed_request("POST", "/fapi/v1/order", {
            "symbol": symbol,
            "side": "SELL" if side == "BUY" else "BUY",
            "type": "MARKET",
            "closePosition": "true"
        })

        return jsonify({
            "status": "closed",
            "closed_position": close_order.json()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
