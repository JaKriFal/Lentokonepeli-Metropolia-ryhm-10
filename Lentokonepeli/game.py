
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/kokeilu/<airport>')
def airports(airport):

    response = {
        'airport': airport
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
