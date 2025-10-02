from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Fake database
books = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A", "available": True},
    {"id": 2, "title": "Cấu trúc dữ liệu", "author": "Trần Thị B", "available": True},
]

loans = []  # danh sách phiếu mượn


# 1 + 2. Client-Server & Stateless
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    token = request.headers.get("Authorization")
    if token != "Bearer library-token":
        return jsonify({"error": "Unauthorized"}), 401

    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Not found"}), 404)


# 3. Cacheable: danh sách sách có thể cache
@app.route("/books", methods=["GET"])
def get_books():
    resp = jsonify(books)
    resp.headers["Cache-Control"] = "public, max-age=60"  # cache 60s
    return resp


# 4. Uniform Interface (CRUD cho books)
@app.route("/books", methods=["POST"])
def create_book():
    data = request.json
    new_id = len(books) + 1
    new_book = {"id": new_id, "title": data["title"], "author": data["author"], "available": True}
    books.append(new_book)
    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    for b in books:
        if b["id"] == book_id:
            b["title"] = data.get("title", b["title"])
            b["author"] = data.get("author", b["author"])
            return jsonify(b)
    return jsonify({"error": "Not found"}), 404


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return "", 204


# API mượn sách
@app.route("/loans", methods=["POST"])
def borrow_book():
    data = request.json
    book_id = data["book_id"]
    user = data["user"]

    book = next((b for b in books if b["id"] == book_id and b["available"]), None)
    if not book:
        return jsonify({"error": "Book not available"}), 400

    book["available"] = False
    loan = {
        "id": len(loans) + 1,
        "book_id": book_id,
        "user": user,
        "borrow_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": None,
    }
    loans.append(loan)
    return jsonify(loan), 201


# API trả sách
@app.route("/loans/<int:loan_id>/return", methods=["PUT"])
def return_book(loan_id):
    for loan in loans:
        if loan["id"] == loan_id and loan["return_date"] is None:
            loan["return_date"] = datetime.now().strftime("%Y-%m-%d")
            book = next((b for b in books if b["id"] == loan["book_id"]), None)
            if book:
                book["available"] = True
            return jsonify(loan)
    return jsonify({"error": "Loan not found"}), 404


# 5. Layered System: middleware giả lập proxy
@app.before_request
def add_proxy_header():
    if "X-Forwarded-For" not in request.headers:
        request.headers.environ["HTTP_X_FORWARDED_FOR"] = "127.0.0.1"


# 6. Code on Demand: server gửi script JS
@app.route("/script.js", methods=["GET"])
def send_script():
    js_code = "alert('Chào mừng bạn đến với hệ thống thư viện RESTful!');"
    return js_code, 200, {"Content-Type": "application/javascript"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
