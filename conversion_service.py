from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

EXCHANGE_RATE_SERVICE_URL = "http://10.6.1.43:6000/rate"  # Update with actual IP of your Exchange Service (VM1)

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    amount = data.get('amount')
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')
    
    if not amount or not from_currency or not to_currency:
        return jsonify({"error": "Amount, from_currency, and to_currency are required"}), 400

    # Get exchange rates from the Exchange Service
    from_rate_response = requests.get(f"{EXCHANGE_RATE_SERVICE_URL}/{from_currency}")
    to_rate_response = requests.get(f"{EXCHANGE_RATE_SERVICE_URL}/{to_currency}")
    
    if from_rate_response.status_code != 200 or to_rate_response.status_code != 200:
        return jsonify({"error": "Invalid currency"}), 400
    
    from_rate = from_rate_response.json().get("rate")
    to_rate = to_rate_response.json().get("rate")
    
    converted_amount = (amount / from_rate) * to_rate
    return jsonify({
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "converted_amount": round(converted_amount, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
