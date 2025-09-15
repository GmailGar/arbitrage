from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Загружаем контракты из JSON
with open('token_contracts.json', 'r') as f:
    token_contracts = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    contract = None
    trade_link = None
    deposit_link = None

    if request.method == 'POST':
        token = request.form.get('token_name', '').strip()
        if token in token_contracts:
            contract = token_contracts[token]
            trade_link = f"https://www.lbank.com/trade/{token.lower()}_usdt"
            deposit_link = f"https://www.lbank.com/wallet/account/main/deposit/crypto/{token.lower()}/solana"

    return render_template('index.html', token=token, contract=contract, trade_link=trade_link, deposit_link=deposit_link)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    iteration = data.get('iteration')
    opportunities = data.get('opportunities', [])
    
    # Добавляем контракты и ссылки к данным
    enriched_opportunities = []
    for opp in opportunities:
        token_name = opp['token_name']
        if token_name in token_contracts:
            opp['contract'] = token_contracts[token_name]
            opp['trade_link'] = f"https://www.lbank.com/trade/{token_name.lower()}_usdt"
            opp['deposit_link'] = f"https://www.lbank.com/wallet/account/main/deposit/crypto/{token_name.lower()}/solana"
        enriched_opportunities.append(opp)
    
    return jsonify({'status': 'success', 'iteration': iteration, 'opportunities': enriched_opportunities}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)