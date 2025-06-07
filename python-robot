import time
import hmac
import hashlib
import requests
import random
import string

# === API Key و Secret ===
api_key = 'zW8tp2oRT18LLDbQ6DW7jcCpgkZoP5KhdJUm11W2SzGYc33KgkFkZpaYKrLSvn2p'
api_secret = 'NRDCiliujMUds2RbRZsTZpkWDINjtL7PUkyVUXIyLljoau8QOy4CfCryrPpJbvoB'

# === آدرس API برای فیوچرز ===
base_url = 'https://api.toobit.com/api/v1/futures/order'

# === تنظیمات سفارش ===
symbol = 'AVAX-SWAP-USDT'
side = 'SELL_OPEN'  # پوزیشن Short
order_type = 'LIMIT'  # اجباری برای ارسال، حتی با priceType
price_type = 'MARKET'
quantity = 1
recvWindow = 10000000
timestamp = int(time.time() * 1000)

# === گرفتن قیمت مارکت ===
def get_mark_price():
    url = 'https://api.toobit.com/quote/v1/markPrice'
    params = {'symbol': symbol}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return float(res.json()['price'])
    else:
        print("❌ خطا در دریافت قیمت مارکت")
        return None

mark_price = get_mark_price()
if not mark_price:
    exit()

# === محاسبه Take Profit و Stop Loss برای پوزیشن SHORT ===
take_profit = round(mark_price * 0.98, 4)  # ۲٪ کاهش برای سود
stop_loss = round(mark_price * 1.04, 4)     # ۴٪ افزایش برای جلوگیری از ضرر

# === شناسه یکتا برای سفارش ===
def generate_client_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

new_client_order_id = generate_client_order_id()

# === ساخت پارامترها ===
params = {
    'symbol': symbol,
    'side': side,
    'type': order_type,
    'priceType': price_type,
    'quantity': quantity,
    'recvWindow': recvWindow,
    'timestamp': timestamp,
    'newClientOrderId': new_client_order_id,
    'takeProfit': str(take_profit),
    'stopLoss': str(stop_loss)
}

# === ساخت رشته امضا و افزودن امضا ===
query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
params['signature'] = signature

# === ارسال درخواست ===
headers = {
    'X-BB-APIKEY': api_key
}
response = requests.post(base_url, headers=headers, data=params)

# === نمایش نتیجه ===
print(response.json())
