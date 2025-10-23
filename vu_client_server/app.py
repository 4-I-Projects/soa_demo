from flask import Flask, jsonify, request

app = Flask(__name__)


books = [
    {"id": 1, "title": "Lap Trinh Python", "author": "Lung Thi Linh", "available": True},
    {"id": 2, "title": "Flask Web Development", "author": "Le Quy Don", "available": True},
]

loans = []


@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),
        "author": data.get("author"),
        "available": True
    }
    books.append(new_book)
    return jsonify({"message": "Book added successfully!", "book": new_book}), 201


@app.route("/api/loans", methods=["POST"])
def borrow_book():
    data = request.get_json()
    book_id = data.get("bookId")
    borrower = data.get("borrower")

    # Tìm sách theo ID
    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                return jsonify({"error": "Book already borrowed!"}), 400

            book["available"] = False
            loans.append({"bookId": book_id, "borrower": borrower})
            return jsonify({"message": f"{borrower} borrowed {book['title']}"}), 200

    return jsonify({"error": "Book not found"}), 404


@app.route("/api/returns/<int:book_id>", methods=["PUT"])
def return_book(book_id):
    for loan in loans:
        if loan["bookId"] == book_id:
            loans.remove(loan)
            for book in books:
                if book["id"] == book_id:
                    book["available"] = True
                    return jsonify({"message": f"{book['title']} returned successfully!"}), 200

    return jsonify({"error": "Loan record not found"}), 404


@app.route("/api/loans", methods=["GET"])
def get_loans():
    return jsonify(loans), 200

if __name__ == "__main__":
    app.run(debug=True)
