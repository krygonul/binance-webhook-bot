@echo off
echo [1/3] Webhook sunucusu başlatılıyor...
start cmd /k "python webhook_server.py"

timeout /t 5 >nul

echo [2/3] LocalTunnel bağlantısı kuruluyor...
start cmd /k "lt --port 5000 --subdomain nice-doors-unite"

echo [3/3] Tüm sistem hazır! TradingView'dan gelen alarmlar işlenmeye hazır.
pause
