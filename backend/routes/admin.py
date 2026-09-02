from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from sqlalchemy import func

from database.db import db
from models.user import User
from models.verification import Verification


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


def get_admin():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return None

    if user.role != "admin":
        return None

    return user


@admin_bp.get("/dashboard")
@jwt_required()
def dashboard():

    admin = get_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    total_users = User.query.count()

    active_users = User.query.filter_by(
        is_active=True
    ).count()

    total_verifications = Verification.query.count()

    genuine = Verification.query.filter_by(
        result="Genuine"
    ).count()

    forged = Verification.query.filter_by(
        result="Forged"
    ).count()

    average_confidence = db.session.query(
        func.avg(Verification.confidence)
    ).scalar()

    return jsonify({
        "users": total_users,
        "active_users": active_users,
        "verifications": total_verifications,
        "genuine": genuine,
        "forged": forged,
        "average_confidence": round(
            float(average_confidence or 0),
            2
        )
    })


@admin_bp.get("/users")
@jwt_required()
def users():

    admin = get_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    records = User.query.order_by(
        User.created_at.desc()
    ).all()

    return jsonify({
        "users": [
            user.to_dict()
            for user in records
        ]
    })


@admin_bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id):

    admin = get_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found."
        }), 404

    data = request.get_json() or {}

    if "role" in data:

        if data["role"] in ["user", "admin"]:
            user.role = data["role"]

    if "is_active" in data:
        user.is_active = bool(
            data["is_active"]
        )

    db.session.commit()

    return jsonify({
        "message": "User updated successfully.",
        "user": user.to_dict()
    })


@admin_bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):

    admin = get_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found."
        }), 404

    if user.id == admin.id:
        return jsonify({
            "error": "You cannot delete your own account."
        }), 400

    Verification.query.filter_by(
        user_id=user.id
    ).delete()

    db.session.delete(user)

    db.session.commit()

    return jsonify({
        "message": "User deleted successfully."
    })


@admin_bp.get("/verifications")
@jwt_required()
def all_verifications():

    admin = get_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    records = Verification.query.order_by(
        Verification.created_at.desc()
    ).all()

    result = []

    for record in records:

        item = record.to_dict()

        item["user"] = {
            "id": record.user.id,
            "name": record.user.name,
            "email": record.user.email
        }

        result.append(item)

    return jsonify({
        "verifications": result
    })