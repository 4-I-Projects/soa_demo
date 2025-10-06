from flask import Blueprint, request, jsonify, url_for
from services.book_service import create_book, get_books_paginated, get_book, update_book, delete_book


books_bp = Blueprint("books_bp", __name__)

@books_bp.route("", methods=["GET"])
def list_books():
    # filters: ?author=...&genre=...&available=true
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    filters = {
        "author": request.args.get("author"),
        "genre": request.args.get("genre"),
        "available": request.args.get("available")
    }
    items, total, pages = get_books_paginated(filters, page, per_page)
    payload = {
        "books": [b.to_dict() for b in items],
        "meta": {"page": page, "per_page": per_page, "total": total, "pages": pages},
        "_links": {
            "self": url_for("books_bp.list_books", page=page, per_page=per_page),
            "create": url_for("books_bp.create_book")
        }
    }
    return jsonify(payload), 200

@books_bp.route("", methods=["POST"])
def create_book():
    data = request.get_json() or {}
    book = create_book(data)
    resp = {
        "message": "Book created",
        "book": book.to_dict(),
        "_links": {
            "self": url_for("books_bp.get_book", book_id=book.id),
            "all": url_for("books_bp.list_books")
        }
    }
    return jsonify(resp), 201

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    resp = {"book": book.to_dict(), "_links": {"all": url_for("books_bp.list_books")}}
    return jsonify(resp), 200

@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book_route(book_id):
    data = request.get_json() or {}
    book = update_book(book_id, data)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Updated", "book": book.to_dict()}), 200

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book_route(book_id):
    ok = delete_book(book_id)
    if not ok:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Deleted"}), 200
