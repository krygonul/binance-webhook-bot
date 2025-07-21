@echo off
cd /d %~dp0binance_webhook_bot
start cmd /k "python webhook_server.py"
start cmd /k "lt --port 5000 --subdomain clean-tools-retire"
