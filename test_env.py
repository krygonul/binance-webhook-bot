import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

print("API_KEY:", API_KEY)
print("API_SECRET:", API_SECRET)
