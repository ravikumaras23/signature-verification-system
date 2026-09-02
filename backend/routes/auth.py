from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from database.db import db
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.post("/register")
def register():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name:
        return jsonify({
            "error": "Name is required."
        }), 400

    if not email:
        return jsonify({
            "error": "Email is required."
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": "Password must contain at least 6 characters."
        }), 400

    existing = User.query.filter_by(
        email=email
    ).first()

    if existing:
        return jsonify({
            "error": "Email already registered."
        }), 409

    user = User(
        name=name,
        email=email,
        role="user"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Registration successful.",
        "token": token,
        "user": user.to_dict()
    }), 201


@auth_bp.post("/login")
def login():

    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user = User.query.filter_by(
        email=email
    ).first()

    if (
        not user
        or not user.check_password(password)
    ):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    if not user.is_active:
        return jsonify({
            "error": "Account is disabled."
        }), 403

    token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful.",
        "token": token,
        "user": user.to_dict()
    })


@auth_bp.get("/me")
@jwt_required()
def current_user():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get(
        user_id
    )

    if not user:
        return jsonify({
            "error": "User not found."
        }), 404

    return jsonify({
        "user": user.to_dict()
    })


@auth_bp.post("/logout")
@jwt_required()
def logout():

    return jsonify({
        "message": "Logout successful."
    })