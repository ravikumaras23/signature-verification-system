from flask import Blueprint, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from sqlalchemy import func

from database.db import db
from models.verification import Verification


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.get("/summary")
@jwt_required()
def summary():

    user_id = int(
        get_jwt_identity()
    )

    total = Verification.query.filter_by(
        user_id=user_id
    ).count()

    genuine = Verification.query.filter_by(
        user_id=user_id,
        result="Genuine"
    ).count()

    forged = Verification.query.filter_by(
        user_id=user_id,
        result="Forged"
    ).count()

    avg_confidence = db.session.query(
        func.avg(
            Verification.confidence
        )
    ).filter(
        Verification.user_id == user_id
    ).scalar()

    return jsonify({
        "total": total,
        "genuine": genuine,
        "forged": forged,
        "average_confidence": round(
            float(avg_confidence or 0),
            2
        ),
        "genuine_rate": round(
            (
                genuine / total * 100
                if total else 0
            ),
            2
        )
    })


@dashboard_bp.get("/chart")
@jwt_required()
def chart():

    user_id = int(
        get_jwt_identity()
    )

    records = Verification.query.filter_by(
        user_id=user_id
    ).order_by(
        Verification.created_at.asc()
    ).all()

    return jsonify({
        "data": [
            {
                "date": record.created_at.strftime(
                    "%Y-%m-%d"
                ),
                "confidence": record.confidence,
                "result": record.result
            }
            for record in records
        ]
    })