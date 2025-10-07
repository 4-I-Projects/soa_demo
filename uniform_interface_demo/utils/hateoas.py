from flask import url_for

def generate_book_links(book_id=None):
    links = {
        "self": url_for("books_bp.list_books", _external=True),
        "create": url_for("books_bp.create_book", _external=True)
    }
    if book_id:
        links.update({
            "detail": url_for("books_bp.get_book", book_id=book_id, _external=True),
            "update": url_for("books_bp.update_book", book_id=book_id, _external=True),
            "delete": url_for("books_bp.delete_book", book_id=book_id, _external=True)
        })
    return links


def generate_user_links(user_id=None):
    links = {
        "self": url_for("users_bp.list_users", _external=True),
        "create": url_for("users_bp.create_user", _external=True)
    }
    if user_id:
        links.update({
            "detail": url_for("users_bp.get_user", user_id=user_id, _external=True),
            "update": url_for("users_bp.update_user", user_id=user_id, _external=True),
            "delete": url_for("users_bp.delete_user", user_id=user_id, _external=True)
        })
    return links


def generate_loan_links(loan_id=None):
    links = {
        "self": url_for("loans_bp.list_loans", _external=True),
        "create": url_for("loans_bp.create_loan", _external=True)
    }
    if loan_id:
        links.update({
            "detail": url_for("loans_bp.get_loan", loan_id=loan_id, _external=True),
            "update": url_for("loans_bp.update_loan", loan_id=loan_id, _external=True),
            "delete": url_for("loans_bp.delete_loan", loan_id=loan_id, _external=True)
        })
    return links
