from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Загружаем контракты из JSON
with open('token_contracts.json', 'r') as f:
    token_contracts = json.load(f)

# Глобальная переменная для хранения последних данных
latest_data = {'iteration': None, 'opportunities': []}

@app.route('/', methods=['GET'])
def index():
    # Передаем последние полученные данные в шаблон
    return render_template('index.html', 
                         iteration=latest_data['iteration'],
                         opportunities=latest_data['opportunities'])

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    
    iteration = data.get('iteration')
    opportunities = data.get('opportunities', [])
    print(f"Received iteration {iteration}, opportunities: {opportunities}")  # Лог для отладки
    
    # Добавляем контракты и ссылки к данным
    enriched_opportunities = []
    for opp in opportunities:
        token_name = opp['token_name']
        if token_name in token_contracts:
            opp['contract'] = token_contracts[token_name]
            opp['trade_link'] = f"https://www.lbank.com/trade/{token_name.lower()}_usdt"
            opp['deposit_link'] = f"https://www.lbank.com/wallet/account/main/deposit/crypto/{token_name.lower()}/solana"
        enriched_opportunities.append(opp)
    
    # Обновляем глобальную переменную
    global latest_data
    latest_data = {'iteration': iteration, 'opportunities': enriched_opportunities}
    
    return jsonify({'status': 'success', 'iteration': iteration, 'opportunities': enriched_opportunities}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)