import os
import uuid

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from services.retrain_service import SignatureRetrainer


retrain_bp = Blueprint(
    "retrain",
    __name__,
    url_prefix="/api/admin/retrain"
)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def is_allowed(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def current_admin():
    try:
        user_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        return None

    user = User.query.get(user_id)

    if not user:
        return None

    if user.role != "admin":
        return None

    return user


@retrain_bp.post("/")
@jwt_required()
def retrain_model():

    admin = current_admin()

    if not admin:
        return jsonify({
            "error": "Administrator access required."
        }), 403

    genuine_files = request.files.getlist("genuine_images")
    forged_files = request.files.getlist("forged_images")

    if not genuine_files and not forged_files:
        return jsonify({
            "error": "Upload at least one genuine or forged image."
        }), 400

    try:

        # ---------------------------------------------------------
        # Dataset directories
        # ---------------------------------------------------------

        dataset_root = os.path.join(
            current_app.root_path,
            "dataset"
        )

        genuine_path = os.path.join(
            dataset_root,
            "train",
            "genuine"
        )

        forged_path = os.path.join(
            dataset_root,
            "train",
            "forged"
        )

        os.makedirs(genuine_path, exist_ok=True)
        os.makedirs(forged_path, exist_ok=True)

        genuine_saved = 0
        forged_saved = 0

        # ---------------------------------------------------------
        # Save genuine images
        # ---------------------------------------------------------

        for file in genuine_files:

            if not file.filename:
                continue

            if not is_allowed(file.filename):
                continue

            filename = (
                str(uuid.uuid4())
                + "_"
                + file.filename
            )

            file.save(
                os.path.join(
                    genuine_path,
                    filename
                )
            )

            genuine_saved += 1

        # ---------------------------------------------------------
        # Save forged images
        # ---------------------------------------------------------

        for file in forged_files:

            if not file.filename:
                continue

            if not is_allowed(file.filename):
                continue

            filename = (
                str(uuid.uuid4())
                + "_"
                + file.filename
            )

            file.save(
                os.path.join(
                    forged_path,
                    filename
                )
            )

            forged_saved += 1

        # ---------------------------------------------------------
        # Validate uploaded files
        # ---------------------------------------------------------

        if genuine_saved == 0 and forged_saved == 0:
            return jsonify({
                "error": "No valid images were uploaded."
            }), 400

        # ---------------------------------------------------------
        # IMPORTANT:
        # DO NOT USE signature_model.keras FOR RETRAINING.
        #
        # The production model remains untouched.
        #
        # Retraining uses:
        # backend/model/retrain_model.keras
        # ---------------------------------------------------------

        retrain_model_path = os.path.join(
            current_app.root_path,
            "model",
            "retrain_model.keras"
        )

        backup_path = os.path.join(
            current_app.root_path,
            "model",
            "backups"
        )

        os.makedirs(
            os.path.dirname(retrain_model_path),
            exist_ok=True
        )

        # ---------------------------------------------------------
        # Create retrainer using SEPARATE model
        # ---------------------------------------------------------

        retrainer = SignatureRetrainer(
            model_path=retrain_model_path,
            forged_dir=forged_path,
            genuine_dir=genuine_path,
            backup_dir=backup_path
        )

        # ---------------------------------------------------------
        # Epochs
        # ---------------------------------------------------------

        epochs = request.form.get(
            "epochs",
            10
        )

        try:
            epochs = int(epochs)
        except (ValueError, TypeError):
            epochs = 10

        epochs = max(
            1,
            min(50, epochs)
        )

        # ---------------------------------------------------------
        # Retrain
        # ---------------------------------------------------------

        result = retrainer.retrain(
            epochs=epochs
        )

        # ---------------------------------------------------------
        # Response
        # ---------------------------------------------------------

        return jsonify({
            "message": "Retraining model trained successfully.",
            "uploaded": {
                "genuine": genuine_saved,
                "forged": forged_saved
            },
            "training": result
        }), 200

    except Exception as error:

        current_app.logger.exception(
            "Retraining failed"
        )

        return jsonify({
            "error": f"Retraining failed: {str(error)}"
        }), 500