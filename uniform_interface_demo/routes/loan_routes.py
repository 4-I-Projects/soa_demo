from flask import Blueprint, request, jsonify, url_for
from services.loan_service import borrow_book, return_book, get_loan
from models.loan import Loan

loans_bp = Blueprint("loans_bp", __name__)

@loans_bp.route("", methods=["POST"])
def create_loan():
    """
    Body: { "user_id": 1, "book_id": 2, "days": 14 }
    """
    data = request.get_json() or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    days = data.get("days", 14)
    loan = borrow_book(user_id, book_id, days)
    if "error" in loan:
        return jsonify(loan), 400
    return jsonify({"message": "Borrowed", "loan": loan.to_dict(), "_links": {"return": url_for("loans_bp.return_loan", loan_id=loan.id)}}), 200

@loans_bp.route("/<int:loan_id>/return", methods=["PUT"])
def return_loan(loan_id):
    res = return_book(loan_id)
    if "error" in res:
        return jsonify(res), 400
    return jsonify({"message": "Returned", "loan": res.to_dict()}), 200

@loans_bp.route("/<int:loan_id>", methods=["GET"])
def get_loan_route(loan_id):
    loan = get_loan(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify({"loan": loan.to_dict(), "_links": {"user": url_for("users_bp.get_user", user_id=loan.user_id)}}), 200
