from binance.client import Client
from binance.enums import *
import time

# === TESTNET API BİLGİLERİ ===
api_key = '042342f7887c82aeffb6cd55972e68c91dacf51a32eb132b2e3d5b5eed014838'
api_secret = '1f75f753478a6a3f40d715abbc31dd4db2551c86b111291261a5e1e04b14dc47'

# === Binance Client (TESTNET) ===
client = Client(api_key, api_secret, testnet=True)
symbol = "DOGEUSDT"

print("🔍 Emirler kontrol ediliyor...\n")

# === 1. Açık Emirleri Göster ===
open_orders = client.futures_get_open_orders(symbol=symbol)

if not open_orders:
    print("📭 Hiçbir açık emir (TP/SL) bulunamadı.\n")
else:
    print("📋 Aktif TP/SL Emirleri:")
    for order in open_orders:
        print(f" → {order['type']} | {order['side']} | Fiyat: {order['price']} | Miktar: {order['origQty']}")
    print("\n❌ Tüm açık emirler iptal ediliyor...")
    cancel = client.futures_cancel_all_open_orders(symbol=symbol)
    print("✅ Emirler iptal edildi.\n")
    time.sleep(1)

# === 2. Açık Pozisyonu Tespit Et ===
try:
    positions = client.futures_position_information(symbol=symbol)
    position = next(p for p in positions if float(p['positionAmt']) != 0)
    side = SIDE_SELL if float(position['positionAmt']) > 0 else SIDE_BUY
    quantity = abs(float(position['positionAmt']))
    print(f"📈 Açık pozisyon bulundu: {'LONG' if side == SIDE_SELL else 'SHORT'} | Miktar: {quantity}")

    # === 3. Mark Fiyat ve LIMIT Emir Fiyatı ===
    mark_price_info = client.futures_mark_price(symbol=symbol)
    mark_price = float(mark_price_info['markPrice'])
    price = round(mark_price * (0.999 if side == SIDE_SELL else 1.001), 5)

    print(f"🎯 Kapanış fiyatı: {price}")

    # === 4. Pozisyonu ReduceOnly Limit Order ile Kapat ===
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type=ORDER_TYPE_LIMIT,
        quantity=quantity,
        price=str(price),
        timeInForce=TIME_IN_FORCE_GTC,
        reduceOnly=True
    )

    print("\n✅ Pozisyon kapatma emri gönderildi:")
    print(f" → Emir ID: {order['orderId']}")
    print(f" → Yön: {order['side']} | Fiyat: {order['price']} | Miktar: {order['origQty']}")
except StopIteration:
    print("ℹ️ Açık pozisyon bulunamadı, işlem yapılmadı.")
except Exception as e:
    print("❌ Hata:", str(e))
