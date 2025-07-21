@echo off
set /p url="Localtunnel webhook adresini gir (https ile): "
curl -X POST %url%/webhook -H "Content-Type: application/json" -d "{\"symbol\":\"BTCUSDT\",\"side\":\"BUY\",\"quantity\":0.05}"
pause