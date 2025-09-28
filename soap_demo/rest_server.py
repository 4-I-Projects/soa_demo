from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập dữ liệu
orders = [
    {"id": 1, "item": "Laptop", "quantity": 1, "price": 1000},
    {"id": 2, "item": "Phone",  "quantity": 2, "price": 500},
]

#REST endpoint: GET /orders
@app.route('/orders', methods=['GET'])
def get_orders():
    token = request.headers.get('Authorization')
    if token != "This is my token":
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(orders)

if __name__ == '__main__':
    app.run(port=3636, debug=True)