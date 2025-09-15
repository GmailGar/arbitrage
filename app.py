from flask import Flask, render_template_string
import json

app = Flask(__name__)

# Загрузка данных из token_contracts.json
with open('token_contracts.json', 'r') as file:
    tokens_data = json.load(file)

# HTML-шаблон для отображения токенов и контрактов
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список токенов и контрактов</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f9;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #e6f3ff;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Список токенов и их контрактов</h1>
        <table>
            <tr>
                <th>Токен</th>
                <th>Контракт</th>
            </tr>
            {% for token, contract in tokens %}
            <tr>
                <td>{{ token }}</td>
                <td>{{ contract }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Передаем данные в шаблон
    return render_template_string(HTML_TEMPLATE, tokens=tokens_data.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)