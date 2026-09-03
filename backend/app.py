import os

from flask import (
    Flask,
    jsonify
)

from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db

from models.user import User

from routes.auth import auth_bp
from routes.verification import verification_bp
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from routes.admin import admin_bp
from routes.retrain import retrain_bp

def create_app():

    app = Flask(
        __name__
    )

    app.config.from_object(
        Config
    )

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        app.config["REPORT_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "database"
        ),
        exist_ok=True
    )

    
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "https://signature-verification-system-ruby.vercel.app",
                    "https://signature-verification-system-d2s5emzrj-ravi-6a21.vercel.app",
                    r"https://.*\.vercel\.app",
                    "http://localhost:5173"
                ]
            }
        },
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    db.init_app(
        app
    )

    JWTManager(
        app
    )

    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        verification_bp
    )

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        reports_bp
    )

    app.register_blueprint(
        admin_bp
    )

    app.register_blueprint(
        retrain_bp
    )

    with app.app_context():

        db.create_all()

        admin_email = "admin@signatureverify.com"

        admin = User.query.filter_by(
            email=admin_email
        ).first()

        if not admin:

            admin = User(
                name="System Administrator",
                email=admin_email,
                role="admin",
                is_active=True
            )

            admin.set_password(
                "Admin@123"
            )

            db.session.add(
                admin
            )

            db.session.commit()

    @app.get("/api/health")
    def health():

        return jsonify({
            "status": "ok",
            "service": "Signature Verification API"
        })

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )