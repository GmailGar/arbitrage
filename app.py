import os
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Загружаем контракты из JSON (замените на свой файл или API)
with open('token_contracts.json', 'r') as f:
    token_contracts = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    contract = None
    trade_link = None
    deposit_link = None

    if request.method == 'POST':
        token = request.form.get('token_name', '').strip().lower()
        if token in token_contracts:
            contract = token_contracts[token]
            trade_link = f"https://www.lbank.com/trade/{token}_usdt"
            deposit_link = f"https://www.lbank.com/wallet/account/main/deposit/crypto/{token}/solana"

    return render_template('index.html', token=token, contract=contract, trade_link=trade_link, deposit_link=deposit_link)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)