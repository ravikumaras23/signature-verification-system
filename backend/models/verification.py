from datetime import datetime

from database.db import db


class Verification(db.Model):
    __tablename__ = "verifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    result = db.Column(
        db.String(30),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    genuine_probability = db.Column(
        db.Float,
        nullable=False
    )

    forged_probability = db.Column(
        db.Float,
        nullable=False
    )

    image_path = db.Column(
        db.String(500),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "verifications",
            lazy=True
        )
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "result": self.result,
            "confidence": round(
                self.confidence,
                2
            ),
            "genuine_probability": round(
                self.genuine_probability,
                2
            ),
            "forged_probability": round(
                self.forged_probability,
                2
            ),
            "image_path": self.image_path,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }