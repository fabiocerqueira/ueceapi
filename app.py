import os
from flask import Flask, jsonify

from model import RU


app = Flask(__name__)


@app.route('/api/ru/menu')
def ru_menu():
    ru = RU()
    json = ru.get_menu()
    return jsonify(json)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
