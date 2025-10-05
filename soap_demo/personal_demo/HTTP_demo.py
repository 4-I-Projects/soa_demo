from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake database
books = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A", "available": True},
    {"id": 2, "title": "Cấu trúc dữ liệu", "author": "Trần Thị B", "available": True},
]


# -------------------------------
# 1. GET - Lấy danh sách hoặc chi tiết sách
# -------------------------------
@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(books)


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Not found"}), 404)


# -------------------------------
# 2. POST - Thêm sách mới
# -------------------------------
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    new_id = len(books) + 1
    book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "available": True,
    }
    books.append(book)
    return jsonify(book), 201


# -------------------------------
# 3. PUT - Cập nhật toàn bộ thông tin sách
# -------------------------------
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    for b in books:
        if b["id"] == book_id:
            b["title"] = data["title"]
            b["author"] = data["author"]
            return jsonify(b)
    return jsonify({"error": "Not found"}), 404


# -------------------------------
# 4. PATCH - Cập nhật một phần thông tin sách
# -------------------------------
@app.route("/books/<int:book_id>", methods=["PATCH"])
def patch_book(book_id):
    data = request.json
    for b in books:
        if b["id"] == book_id:
            if "title" in data:
                b["title"] = data["title"]
            if "author" in data:
                b["author"] = data["author"]
            return jsonify(b)
    return jsonify({"error": "Not found"}), 404


# -------------------------------
# 5. DELETE - Xóa sách
# -------------------------------
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return "", 204


# -------------------------------
# 6. OPTIONS - Trả về các method được hỗ trợ
# -------------------------------
@app.route("/books", methods=["OPTIONS"])
def options_books():
    return "", 200, {"Allow": "GET,POST,OPTIONS"}


# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
