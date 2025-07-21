@echo off
cd /d "%~dp0"
echo [♻️] Sanal ortam aktifleştiriliyor...
call venv\Scripts\activate.bat
echo [📦] Paketler yükleniyor...
pip install -q -r requirements.txt
echo [🚀] Flask bot başlatılıyor...
set FLASK_ENV=development
set PYTHONUNBUFFERED=1
python app.py
pause
