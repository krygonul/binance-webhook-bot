from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import math

load_dotenv()

app = Flask(__name__)

# Binance API ayarları
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSWORD = os.getenv("PASSWORD", "seninsifren")

client = Client(API_KEY, API_SECRET)

# Pozisyon büyüklüğü hesaplama
def calculate_quantity(symbol, entry_price, risk_percent):
    balance = client.futures_account_balance()
    usdt_balance = next((float(x["balance"]) for x in balance if x["asset"] == "USDT"), 0.0)
    risk_amount = usdt_balance * (risk_percent / 100)
    quantity = risk_amount / entry_price
    return round(quantity, 2)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("📥 Alındı:", data)

        if data is None:
            return jsonify({"error": "Geçersiz JSON"}), 400

        if data.get("password") != PASSWORD:
            return jsonify({"error": "Şifre yanlış"}), 403

        symbol = data.get("symbol")
        side = data.get("side")
        tp = float(data.get("tp"))
        sl = float(data.get("sl"))

        if not all([symbol, side, tp, sl]):
            return jsonify({"error": "Eksik veri alanı"}), 400

        # Fiyatları al
        ticker = client.futures_symbol_ticker(symbol=symbol)
        entry_price = float(ticker["price"])

        # Miktar hesapla (%21 risk)
        quantity = calculate_quantity(symbol, entry_price, 21)

        # Pozisyon aç
        order_side = SIDE_BUY if side == "buy" else SIDE_SELL
        opposite_side = SIDE_SELL if side == "buy" else SIDE_BUY

        # Piyasa emri
        order = client.futures_create_order(
            symbol=symbol,
            side=order_side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )

        # TP ve SL seviyeleri
        tp_price = round(entry_price + tp, 5) if side == "buy" else round(entry_price - tp, 5)
        sl_price = round(entry_price - sl, 5) if side == "buy" else round(entry_price + sl, 5)

        # TP emri (limit)
        client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type=ORDER_TYPE_LIMIT,
            quantity=quantity,
            price=tp_price,
            timeInForce=TIME_IN_FORCE_GTC
        )

        # SL emri (stop market)
        client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type=ORDER_TYPE_STOP_MARKET,
            stopPrice=sl_price,
            closePosition=True,
            timeInForce=TIME_IN_FORCE_GTC
        )

        print(f"✅ Binance emri gönderildi: {side.upper()} {symbol} @ {entry_price} / Miktar: {quantity}")
        return jsonify({"message": "Emir başarıyla işlendi."}), 200

    except Exception as e:
        print("❌ HATA:", str(e))
        return jsonify({"error": "Sunucu hatası", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
