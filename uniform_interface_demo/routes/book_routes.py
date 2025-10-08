from flask import Blueprint, request, jsonify, url_for
from services.book_service import create_book, get_books_paginated, get_book, update_book, delete_book
from utils.hateoas import generate_book_links

books_bp = Blueprint("books_bp", __name__)

@books_bp.route("", methods=["GET"], endpoint="list_books")
def list_books():
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
        "_links": generate_book_links()
    }
    return jsonify(payload), 200


@books_bp.route("", methods=["POST"], endpoint="create_book")
def create_book_route():
    data = request.get_json() or {}
    book = create_book(data)
    resp = {
        "message": "Book created",
        "book": book.to_dict(),
        "_links": generate_book_links(book.id)
    }
    return jsonify(resp), 201


@books_bp.route("/<int:book_id>", methods=["GET"], endpoint="get_book")
def get_book_route(book_id):
    book = get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    resp = {
        "book": book.to_dict(),
        "_links": generate_book_links(book.id)
    }
    return jsonify(resp), 200


@books_bp.route("/<int:book_id>", methods=["PUT"], endpoint="update_book")
def update_book_route(book_id):
    data = request.get_json() or {}
    book = update_book(book_id, data)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "message": "Book updated",
        "book": book.to_dict(),
        "_links": generate_book_links(book.id)
    }), 200


@books_bp.route("/<int:book_id>", methods=["DELETE"], endpoint="delete_book")
def delete_book_route(book_id):
    ok = delete_book(book_id)
    if not ok:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "message": "Book deleted",
        "_links": generate_book_links()
    }), 200
