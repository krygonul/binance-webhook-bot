import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # TLS protokolünü zorla
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount("https://", TLSAdapter())

try:
    r = session.get("https://api.binance.com/api/v3/ping", timeout=10)
    print("✅ Yanıt:", r.text)
except Exception as e:
    print("❌ Hata:", e)
