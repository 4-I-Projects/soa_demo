from flask import Blueprint, request, jsonify, url_for
from database import db
from models.user import User
from models.book import Book

users_bp = Blueprint("users_bp", __name__)

@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "name and email required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 400
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User created",
        "user": user.to_dict(),
        "_links": {
            "self": url_for("users_bp.get_user", user_id=user.id, _external=True),
            "all": url_for("users_bp.list_users", _external=True)
        }
    }), 201

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    borrowed = [loan.to_dict() for loan in user.loans]
    return jsonify({"user": user.to_dict(), "loans": borrowed, "_links": {"all_users": url_for("users_bp.create_user")}}), 200

@users_bp.route("", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify({
        "users": [u.to_dict() for u in users],
        "_links": {
            "self": url_for("users_bp.list_users", _external=True),
            "create": url_for("users_bp.create_user", _external=True)
        }
    }), 200
    
@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user_id:
            return jsonify({"error": "Email already in use"}), 400
        user.email = data["email"]
    db.session.commit()
    return jsonify({"message": "User updated", "user": user.to_dict()}), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.loans:
        return jsonify({"error": "Cannot delete user with active loans"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200