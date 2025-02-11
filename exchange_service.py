from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database for currency rates
exchange_rates = {
    "USD": 1.0,  # Base currency is USD
    "EUR": 0.85,
    "JPY": 110.0,
    "INR": 75.0
}

@app.route('/rate/<currency>', methods=['GET'])
def get_rate(currency):
    rate = exchange_rates.get(currency.upper())
    if rate is None:
        return jsonify({"error": "Currency not found"}), 404
    return jsonify({"currency": currency.upper(), "rate": rate})

@app.route('/rate', methods=['POST'])
def update_rate():
    data = request.get_json()
    currency = data.get('currency')
    rate = data.get('rate')
    
    if not currency or not rate:
        return jsonify({"error": "Currency and rate are required"}), 400
    
    exchange_rates[currency.upper()] = rate
    return jsonify({"message": f"Exchange rate for {currency.upper()} updated to {rate}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
