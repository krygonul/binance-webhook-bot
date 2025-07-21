@echo off
title Binance Webhook Süper Başlatıcı
setlocal

set "SYMBOL=BTCUSDT"
set "SIDE=BUY"
set "QUANTITY=0.05"

echo [1/5] Python paketleri kuruluyor...
py -3.11 -m pip install --upgrade pip >nul
py -3.11 -m pip install flask requests python-dotenv >nul

echo [2/5] Webhook sunucusu başlatiliyor...
start "" /min py -3.11 webhook_server.py
timeout /t 2 >nul

echo [3/5] Localtunnel terminalde açılıyor...
start "" cmd /k "npx localtunnel --port 5000"
timeout /t 6 >nul
set /p LT_URL=🔗 Lütfen localtunnel linkini buraya yapıştır: 

echo [4/5] Webhook gönderiliyor...
curl -X POST %LT_URL%/webhook -H "Content-Type: application/json" -d "{\"symbol\":\"%SYMBOL%\",\"side\":\"%SIDE%\",\"quantity\":%QUANTITY%}"

echo.
echo [5/5] ✅ İşlem tamamlandı.
endlocal
