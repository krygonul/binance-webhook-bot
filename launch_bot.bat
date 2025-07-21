@echo off
echo [1/3] Python Flask sunucusu başlatılıyor...
start cmd /k python webhook_server.py

echo [2/3] Ngrok başlatılıyor...
start cmd /k ngrok http 5000

echo [3/3] Her şey hazır. Webhook URL'ni ngrok ekranından kopyala!
pause