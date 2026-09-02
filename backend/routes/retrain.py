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

from models.user import User
from services.retrain_service import (
    SignatureRetrainer
)


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

    extension = (
        filename
        .rsplit(".", 1)[1]
        .lower()
    )

    return extension in ALLOWED_EXTENSIONS


def current_admin():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get(
        user_id
    )

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
            "error":
                "Administrator access required."
        }), 403


    genuine_files = (
        request.files.getlist(
            "genuine_images"
        )
    )

    forged_files = (
        request.files.getlist(
            "forged_images"
        )
    )


    if (
        not genuine_files
        and not forged_files
    ):

        return jsonify({
            "error":
                "Upload at least one genuine or forged image."
        }), 400


    try:

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


        os.makedirs(
            genuine_path,
            exist_ok=True
        )

        os.makedirs(
            forged_path,
            exist_ok=True
        )


        genuine_saved = 0
        forged_saved = 0


        for file in genuine_files:

            if not file.filename:
                continue

            if not is_allowed(
                file.filename
            ):
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


        for file in forged_files:

            if not file.filename:
                continue

            if not is_allowed(
                file.filename
            ):
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


        if (
            genuine_saved == 0
            and forged_saved == 0
        ):

            return jsonify({
                "error":
                    "No valid images were uploaded."
            }), 400


        model_path = (
            current_app.config[
                "MODEL_PATH"
            ]
        )


        backup_path = os.path.join(
            current_app.root_path,
            "model",
            "backups"
        )


        retrainer = SignatureRetrainer(
            model_path=model_path,
            dataset_path=dataset_root,
            backup_path=backup_path
        )


        epochs = request.form.get(
            "epochs",
            10
        )

        try:
            epochs = int(epochs)
        except ValueError:
            epochs = 10


        epochs = max(
            1,
            min(50, epochs)
        )


        result = retrainer.retrain(
            epochs=epochs
        )


        return jsonify({
            "message":
                "Model retrained successfully.",
            "uploaded": {
                "genuine":
                    genuine_saved,
                "forged":
                    forged_saved
            },
            "training": result
        })


    except Exception as error:

        return jsonify({
            "error":
                f"Retraining failed: {str(error)}"
        }), 500