from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

# Mock data
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
    {"id": 2, "title": "Design Patterns", "author": "GoF", "available": True}
]

users = [
    {"id": 1, "name": "Alice", "borrowed": []},
    {"id": 2, "name": "Bob", "borrowed": []}
]


# --- 1. Resource identification (GET all books) ---
@app.route("/books", methods=["GET"])
def get_books():
    response = {
        "books": books,
        "_links": {
            "self": url_for("get_books"),
            "create": url_for("add_book")
        }
    }
    return jsonify(response), 200


# --- 2. Manipulation through representation (POST) ---
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = {"id": new_id, "title": data["title"], "author": data["author"], "available": True}
    books.append(new_book)
    response = {
        "message": "Book added",
        "book": new_book,
        "_links": {
            "self": url_for("get_book", book_id=new_id),
            "all_books": url_for("get_books")
        }
    }
    return jsonify(response), 201


# --- 3. Self-descriptive message (GET by ID, proper status codes) ---
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        response = {
            "book": book,
            "_links": {
                "borrow": url_for("borrow_book", user_id=1, book_id=book_id),  # giả định user=1
                "all_books": url_for("get_books")
            }
        }
        return jsonify(response), 200
    return jsonify({"error": "Book not found"}), 404


# --- 4. Borrowing a book (PUT) ---
@app.route("/users/<int:user_id>/borrow/<int:book_id>", methods=["PUT"])
def borrow_book(user_id, book_id):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)

    if not user or not book:
        return jsonify({"error": "User or Book not found"}), 404

    if not book["available"]:
        return jsonify({"error": "Book already borrowed"}), 400

    book["available"] = False
    user["borrowed"].append(book_id)

    response = {
        "message": f"{user['name']} borrowed {book['title']}",
        "_links": {
            "return": url_for("return_book", user_id=user_id, book_id=book_id),
            "user": url_for("get_user", user_id=user_id)
        }
    }
    return jsonify(response), 200


# --- Return a book (PUT) ---
@app.route("/users/<int:user_id>/return/<int:book_id>", methods=["PUT"])
def return_book(user_id, book_id):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)

    if not user or not book:
        return jsonify({"error": "User or Book not found"}), 404

    if book_id not in user["borrowed"]:
        return jsonify({"error": "This book was not borrowed by the user"}), 400

    book["available"] = True
    user["borrowed"].remove(book_id)

    response = {
        "message": f"{user['name']} returned {book['title']}",
        "_links": {
            "borrow_again": url_for("borrow_book", user_id=user_id, book_id=book_id),
            "user": url_for("get_user", user_id=user_id)
        }
    }
    return jsonify(response), 200


# --- Get user info ---
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        borrowed_books = [b for b in books if b["id"] in user["borrowed"]]
        response = {
            "user": user,
            "borrowed_books": borrowed_books,
            "_links": {
                "all_books": url_for("get_books")
            }
        }
        return jsonify(response), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
