import os
import uuid

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from werkzeug.utils import secure_filename

from database.db import db
from models.user import User
from models.verification import Verification
from services.prediction import SignaturePredictor


verification_bp = Blueprint(
    "verification",
    __name__,
    url_prefix="/api/verification"
)


predictor = None


def get_predictor():

    global predictor

    if predictor is None:
        predictor = SignaturePredictor(
            current_app.config["MODEL_PATH"]
        )

    return predictor


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in (
        current_app.config[
            "ALLOWED_EXTENSIONS"
        ]
    )


@verification_bp.post("/")
@jwt_required()
def verify_signature():

    user_id = int(
        get_jwt_identity()
    )

    if "file" not in request.files:

        return jsonify({
            "error": "No image file uploaded."
        }), 400

    file = request.files["file"]

    if not file.filename:

        return jsonify({
            "error": "No selected file."
        }), 400

    if not allowed_file(
        file.filename
    ):

        return jsonify({
            "error": "Unsupported image format."
        }), 400

    unique_name = (
        str(uuid.uuid4())
        + "_"
        + secure_filename(
            file.filename
        )
    )

    upload_folder = (
        current_app.config[
            "UPLOAD_FOLDER"
        ]
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    image_path = os.path.join(
        upload_folder,
        unique_name
    )

    file.save(image_path)

    try:

        prediction = get_predictor().predict(
            image_path
        )

        verification = Verification(
            user_id=user_id,
            filename=file.filename,
            result=prediction["label"],
            confidence=prediction["confidence"],
            genuine_probability=prediction[
                "genuine_probability"
            ],
            forged_probability=prediction[
                "forged_probability"
            ],
            image_path=image_path
        )

        db.session.add(
            verification
        )

        db.session.commit()

        return jsonify({
            "message": "Verification completed.",
            "verification": verification.to_dict()
        }), 201

    except Exception as error:

        if os.path.exists(
            image_path
        ):
            os.remove(
                image_path
            )

        return jsonify({
            "error": str(error)
        }), 500


@verification_bp.get("/history")
@jwt_required()
def history():

    user_id = int(
        get_jwt_identity()
    )

    records = Verification.query.filter_by(
        user_id=user_id
    ).order_by(
        Verification.created_at.desc()
    ).all()

    return jsonify({
        "verifications": [
            record.to_dict()
            for record in records
        ]
    })


@verification_bp.get("/<int:verification_id>")
@jwt_required()
def get_verification(
    verification_id
):

    user_id = int(
        get_jwt_identity()
    )

    record = Verification.query.get(
        verification_id
    )

    if not record:
        return jsonify({
            "error": "Verification not found."
        }), 404

    if record.user_id != user_id:
        return jsonify({
            "error": "Access denied."
        }), 403

    return jsonify({
        "verification": record.to_dict()
    })