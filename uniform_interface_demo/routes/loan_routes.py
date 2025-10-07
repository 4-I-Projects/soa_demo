from flask import Blueprint, request, jsonify, url_for
from services.loan_service import borrow_book, return_book, get_loan

loans_bp = Blueprint("loans_bp", __name__)

@loans_bp.route("", methods=["POST"], endpoint="create_loan_route")
def create_loan_route():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    days = data.get("days", 14)
    
    loan = borrow_book(user_id, book_id, days)
    if isinstance(loan, dict) and "error" in loan:
        return jsonify(loan), 400

    return jsonify({
        "message": "Borrowed successfully",
        "loan": loan.to_dict(),
        "_links": {
            "self": url_for("loans_bp.get_loan_route", loan_id=loan.id, _external=True),
            "return": url_for("loans_bp.return_loan_route", loan_id=loan.id, _external=True),
            "user": url_for("users_bp.get_user", user_id=loan.user_id, _external=True),
            "book": url_for("books_bp.get_book", book_id=loan.book_id, _external=True)
        }
    }), 201

@loans_bp.route("/<int:loan_id>/return", methods=["PUT"])
def return_loan_route(loan_id):
    res = return_book(loan_id)
    if isinstance(res, dict) and "error" in res:
        return jsonify(res), 400
    return jsonify({
        "message": "Returned successfully",
        "loan": res.to_dict(),
        "_links": {
            "self": url_for("loans_bp.get_loan_route", loan_id=loan_id, _external=True),
            "all": url_for("loans_bp.list_loans", _external=True)
        }
    }), 200

@loans_bp.route("/<int:loan_id>", methods=["GET"])
def get_loan_route(loan_id):
    loan = get_loan(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify({
        "loan": loan.to_dict(),
        "_links": {
            "return": url_for("loans_bp.return_loan_route", loan_id=loan.id, _external=True),
            "user": url_for("users_bp.get_user", user_id=loan.user_id, _external=True),
            "book": url_for("books_bp.get_book", book_id=loan.book_id, _external=True)
        }
    }), 200

@loans_bp.route("", methods=["GET"])
def list_loans():
    from models.loan import Loan
    loans = Loan.query.all()
    return jsonify({
        "loans": [loan.to_dict() for loan in loans],
        "_links": {
            "self": url_for("loans_bp.list_loans", _external=True),
            "create": url_for("loans_bp.create_loan_route", _external=True)
        }
    }), 200