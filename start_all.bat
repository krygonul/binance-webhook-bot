@echo off
title Binance Webhook Otomatik Başlatıcı

echo [1/4] Python paketleri kuruluyor...
py -3.11 -m pip install --upgrade pip >nul
py -3.11 -m pip install flask requests python-dotenv >nul

echo [2/4] Webhook sunucusu başlatiliyor...
start "" /min py -3.11 webhook_server.py

timeout /t 2 >nul

echo [3/4] Localtunnel aciliyor...
start "" /min npx localtunnel --port 5000

timeout /t 3 >nul

echo [4/4] ✅ Sistem tamamlandi.
echo 🔗 Localtunnel adresi diger pencerede gorulecek.
echo 🔁 Artık TradingView sinyalleri ya da curl ile test edebilirsin.
