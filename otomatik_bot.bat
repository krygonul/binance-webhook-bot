@echo off
title Binance Webhook Bot Otomatik Başlatıcı
echo [1/2] Flask sunucusu başlatılıyor...
start cmd /k "cd /d C:\Users\Derin\Desktop\binance_webhook_bot && python webhook_server.py"

timeout /t 3 > nul

echo [2/2] LocalTunnel başlatılıyor...
start cmd /k "npx localtunnel --port 5000"
