from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook verisi alındı:", data)
    # Örn: burada işlem tetikleyebilirsin
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
