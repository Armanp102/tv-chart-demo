from flask import Flask, request,  send_from_directory, jsonify
from flask_cors import CORS
import os 
import hmac
import hashlib
import requests
import time
import random
import string


app = Flask(__name__)
CORS(app)

# === API Key و Secret ===
api_key = 'zW8tp2oRT18LLDbQ6DW7jcCpgkZoP5KhdJUm11W2SzGYc33KgkFkZpaYKrLSvn2p'
api_secret = 'NRDCiliujMUds2RbRZsTZpkWDINjtL7PUkyVUXIyLljoau8QOy4CfCryrPpJbvoB'
base_url = 'https://api.toobit.com/api/v1/futures/order'

# === این روت برای نمایش فایل HTML ===
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'chart.html')

# === این روت سیگنال‌ها را دریافت می‌کند ===
@app.route('/signal', methods=['POST'])
def receive_signal():
    data = request.get_json()
    signal_type = data['signal']  # 'LONG' یا 'SHORT'
    price = data['price']  # قیمت ارسال‌شده از JavaScript

    print(f"Received signal: {signal_type} at price: {price}")

    # تعیین نوع سفارش بر اساس سیگنال
    if signal_type == "LONG":
        side = "BUY_OPEN"
    elif signal_type == "SHORT":
        side = "SELL_OPEN"
    else:
        return jsonify({"status": "error", "message": "Invalid signal type"})

    # محاسبه Take Profit و Stop Loss
    take_profit = round(price * 1.02, 4)  # ۲٪ افزایش برای سود
    stop_loss = round(price * 0.98, 4)   # ۲٪ کاهش برای جلوگیری از ضرر

    # === شناسه یکتا برای سفارش ===
    def generate_client_order_id():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    new_client_order_id = generate_client_order_id()

    # === ساخت پارامترها ===
    params = {
        'symbol': 'AVAX-SWAP-USDT',
        'side': side,
        'type': 'LIMIT',
        'priceType': 'MARKET',
        'quantity': 1,
        'recvWindow': 10000000,
        'timestamp': int(time.time() * 1000),
        'newClientOrderId': new_client_order_id,
        'takeProfit': str(take_profit),
        'stopLoss': str(stop_loss)
    }

    # === ساخت رشته امضا و افزودن امضا ===
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params['signature'] = signature

    # === ارسال درخواست به API فیوچرز ===
    headers = {
        'X-BB-APIKEY': api_key
    }
    response = requests.post(base_url, headers=headers, data=params)

    # === نمایش نتیجه ===
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
