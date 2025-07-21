@echo off
echo [1/3] Flask sunucusu başlatılıyor...
start cmd /k python webhook_server.py

echo [2/3] Localtunnel açılıyor (port 5000)...
start cmd /k npx localtunnel --port 5000

echo [3/3] Webhook URL'yi üstteki localtunnel ekranından kopyalayabilirsin.
pause