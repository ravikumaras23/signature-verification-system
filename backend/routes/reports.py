import os

from flask import (
    Blueprint,
    send_file,
    jsonify,
    current_app
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models.user import User
from models.verification import Verification
from services.report_service import generate_report


reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/reports"
)


@reports_bp.get(
    "/<int:verification_id>/download"
)
@jwt_required()
def download_report(
    verification_id
):

    user_id = int(
        get_jwt_identity()
    )

    verification = Verification.query.get(
        verification_id
    )

    if not verification:
        return jsonify({
            "error": "Verification not found."
        }), 404

    if verification.user_id != user_id:
        return jsonify({
            "error": "Access denied."
        }), 403

    user = User.query.get(
        user_id
    )

    filename = (
        f"verification_report_"
        f"{verification.id}.pdf"
    )

    output_path = os.path.join(
        current_app.config["REPORT_FOLDER"],
        filename
    )

    generate_report(
        verification,
        user,
        output_path
    )

    return send_file(
        output_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )